import re

from types          import SimpleNamespace
from time           import sleep
from jose           import jwt
from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from quart          import Blueprint
from quart          import current_app
from quart          import render_template
from quart          import request
from quart          import redirect
from quart          import url_for
from quart          import session

from model          import db
from model          import PersonalBaseInformationsTable
from model          import CrewMemberTable
from model          import DutyTable
from model          import RankTable
from model          import DivisionTable
from model          import CrewMemberRankTable
from model          import CrewMemberDutyTable
from model          import CrewMemberDivisionTable
from model          import MemberOnboardLogEntryTable
from model          import MemberRankLogEntryTable
from model          import MemberDivisionLogEntryTable
from model          import MemberTaskLogEntryTable
from model          import MemberMissionLogEntryTable
from model          import selectPerson
from model          import selectCrew
from model          import selectRank
from model          import selectDuty
from model          import selectDivision

from forms          import AddCrewMemberForm
from forms          import RemoveCrewMemberForm
from forms          import EditCrewMemberForm

from authorization  import require_user
from authorization  import require_role
from authorization  import require_login

from permissions    import CrewPermissions

from baseClasses    import Editable
from baseClasses    import Addable

from standardReturn import standardReturn

isAlpha  = r"^[A-Za-z]+$"
isNumber = r"^[0-9]+$"

crew_blueprint = Blueprint("crew",__name__,url_prefix='/crew',template_folder='templates/default')

sectionName = "Crew"

class CrewMember(Editable):
    def __init__(self,source="db",FirstName="",LastName="",Nickname="",Rank="",Division="",Duties=list(),Serial=0,Stic=0):
        self.Error  = ""
        self.source = source
        #TODO: Make it work with keycloack too
        if self.source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crewMemberInformations = s.scalar(selectCrew(self.Nickname))
                    if crewMemberInformations:
                        if re.match(isNumber,crewMemberInformations.Serial):
                            self.Serial = crewMemberInformations.Serial
                        else:
                            self.Error = "Member serial is not a number"
                            raise Exception(self.Error)
                        if re.match(isNumber,crewMemberInformations.Stic):
                            self.Stic   = crewMemberInformations.Stic
                        else:
                            self.Error = "Member STIC membership is not a number"
                            raise Exception(self.Error)
                    else:
                        self.Error = "Crew member not found"
                        raise Exception(self.Error)
        self.FirstName = FirstName
        self.LastName  = LastName
        self.Nickname  = Nickname
        self.Rank      = Rank
        self.Division  = Division
        self.Duties    = Duties

    def edit(self,attributes:dict):
        for key,value in attributes:
            try:
                attribute = getattr(self,key)
                attribute = value
            except Exception as e:
                print(e)
        #TODO: Make it work with keycloack too
        if self.source == "db":
            person             = PersonalBaseInformationsTable(FirstName=self.FirstName,LastName=self.LastName,Nickname=self.Nickname)
            crewMember         = CrewMemberTable(PersonalBaseInformationsId=person.Id)
            crewMemberRank     = CrewMemberRankTable(MemberSerial=crewMember.Serial,RankName=rank)
            crewMemberDivision = CrewMemberDivisionTable(MemberSerial=crewMember.Serial,DivisionName=division)
            crewMemberDuty     = [ CrewMemberDutyTable(MemberSerial=self.Serial,DutyName=duty.name) for duty in self.Duties ]
        with db.bind.Session() as s:
            with s.begin():
                s.commit()
    def load(self,Nickname="",Serial=0):
        #TODO: Make it work with keycloack too
        if self.source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    if Nickname:
                        crewMemberInformations = s.scalar(selectCrew(Nickname))
                    elif Serial:
                        crewMemberInformations = s.scalar(selectCrew(Serial))
                    else:
                        self.Error = "Search clause missing"
                        return
                    if crewMemberInformations:
                        self.FirstName = crewMemberInformations.FirstName
                        self.LastName  = crewMemberInformations.LastName
                        self.Nickname  = crewMemberInformations.Nickname
                        self.Serial    = crewMemberInformations.Serial
                        self.Rank      = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().RankName
                        self.Division  = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().DivisionName
                        self.Duties    = [ duty.Dutyname for duty in s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).all() ]
                        self.Stic      = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().Stic
                    else:
                        self.Error = "Crew member not found"
                        return

class Crew(Addable):
    def __init__(self,source="db"):
        self.source="db"
        self.crew = list()
        #TODO: Make it work with keycloack too
        if self.source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crew = s.scalars(selectCrew()).all()
                    for member in crew:
                        if re.match(member.FirstName,isAlpha) and
                        re.match(member.LastName,isAlpha)     and
                        re.match(member.Nickname,isAlpha)     and
                        re.match(member.Rank,isAlpha)         and
                        re.match(member.Division,isAlpha)     and
                        re.match(member.Duties,isAlpha)       and
                        re.match(member.Serial,isNumber)      and
                        re.match(member.Stic,isNumber):
                            self.crew.append(CrewMember("db",
                                                        member.FirstName,
                                                        member.LastName,
                                                        member.Nickname,
                                                        member.Rank,
                                                        member.Division,
                                                        member.Duties,
                                                        member.Serial,
                                                        member.Stic
                                                    ))
    def add(self,member:CrewMember):
        if re.match(member.FirstName,isAlpha) and
           re.match(member.LastName,isAlpha)  and
           re.match(member.Nickname,isAlpha)  and
           re.match(member.Rank,isAlpha)      and
           re.match(member.Division,isAlpha)  and
           re.match(member.Duties,isAlpha)    and
           re.match(member.Serial,isNumber)   and
           re.match(member.Stic,isNumber):
            #TODO: Make it work with keycloack too
            self.crew.append(CrewMember("db",
                                        member.FirstName,
                                        member.LastName,
                                        member.Nickname,
                                        member.Rank,
                                        member.Division,
                                        member.Duties,
                                        member.Serial,
                                        member.Stic
                                    ))
    def remove(self,member:CrewMember):
        self.crew.remove(member)
    def load(self):
        pass

@crew_blueprint.route("/",methods=["GET"])
@require_login
async def crew():
    crew = list()
    with db.bind.Session() as s:
        with s.begin():
            crew = s.scalars(selectCrew()).all()
    if len(crew) > 0:
        return await standardReturn("crew.html",sectionName,crew=crew)
    else:
        return await standardReturn("error.html",sectionName,error="No crew member found")

@crew_blueprint.route("/member/<member>",methods=["GET"])
async def member(member):
    if require_role(member):
        token = jwt.get_unverified_claims(session['auth_token']['access_token'])
        cm           = SimpleNamespace()
        cm.FirstName = token['given_name']
        cm.LastName  = token['family_name']
        cm.Nickname  = token['preferred_username']
        cm.Rank      = [ i.split("/")[len(i.split("/"))-1] for i in token['groups'] if 'Gradi'     in i ][0]
        cm.Division  = [ i.split("/")[len(i.split("/"))-1] for i in token['groups'] if 'Divisioni' in i ][0]
        cm.Duties    = [ i.split("/")[len(i.split("/"))-1] for i in token['groups'] if 'Doveri'    in i ]
        crewMember = CrewMember(cm.FirstName,cm.LastName,cm.Nickname,cm.Rank,cm.Division,cm.Duties)
        return await standardReturn("crewMember.html",sectionName,CREWMEMBER=cm)

@crew_blueprint.route("/add",methods=["GET","POST"])
@require_role(CrewPermissions.addMemberRole)
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack too
    form   = AddCrewMemberForm()
    if request.method == 'GET':
        ranks     = []
        duties    = []
        divisions = []
        try:
            with db.bind.Session() as s:
                with s.begin():
                    ranks     = s.scalars(selectRank()).all()
                    duties    = s.scalars(selectDuty()).all()
                    divisions = s.scalars(selectDivision()).all()
        except Exception as e:
                return await render_template("error.html",sectionName,error=str(e))
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        return await render_template("crewMemberAdd.html",sectionName,FORM=form)
    elif request.method == 'POST':
        crewMember = CrewMember(FirstName = (await request.form)['FirstName'],
                               LastName  = (await request.form)['LastName'],
                               Nickname  = (await request.form)['Nickname'],
                               Rank      = (await request.form)['Rank'],
                               Division  = (await request.form)['Division'],
                               Duties    = (await request.form)\
                                                              .getlist('Duties')
                           )

        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(personalBaseInformations)
                        s.commit()
                        s.flush()
                with db.bind.Session() as s:
                    with s.begin():
                        person     = s.scalar(selectPerson(nickname))
                        crewMember = CrewMemberTable(PersonalBaseInformationsId=person.Id)
                        s.add(crewMember)
                        s.commit()
                        s.flush()
                with db.bind.Session() as s:
                    with s.begin():
                        person             = s.scalar(selectPerson(nickname))
                        crewMember         = s.scalar(select(CrewMemberTable)\
                                            .where(CrewMemberTable.PersonalBaseInformationsId==person.Id))
                        crewMemberRank     = CrewMemberRankTable(MemberSerial=crewMember.Serial,
                                                                RankName=rank)
                        crewMemberDivision = CrewMemberDivisionTable(MemberSerial=crewMember.Serial,
                                                                    DivisionName=division)
                        s.add(crewMemberRank)
                        s.add(crewMemberDivision)
                        s.commit()
                        s.flush()
                for duty in duties:
                    with db.bind.Session() as s:
                        with s.begin():
                            person         = s.scalar(selectPerson(nickname))
                            crewMember     = s.scalar(select(CrewMemberTable)\
                                            .where(CrewMemberTable.PersonalBaseInformationsId==person.Id))
                            crewMemberDuty = CrewMemberDutyTable(MemberSerial=crewMember.Serial,
                                            DutyName=duty)
                            s.add(crewMemberDuty)
                            s.commit()
                            s.flush()
            except Exception as e:
                return await render_template("error.html",sectionName,error="1: "+str(e))
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        ranks     = s.scalars(selectRank()).all()
                        duties    = s.scalars(selectDuty()).all()
                        divisions = s.scalars(selectDivision()).all()
            except Exception as e:
                    return await render_template("error.html",sectionName,error="2: "+str(e))
            form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
            form.Duties.choices   = [(d.Name,d.Name) for d in duties]
            form.Division.choices = [(d.Name,d.Name) for d in divisions]
            return await render_template("crewMemberAdd.html",
                                         sectionName,
                                         FORM=form,
                                         DUTIES=duties,
                                         MESSAGE='Success')
    else:
        return await render_template("error.html",sectionName,error="Invalid method")

@crew_blueprint.route("/remove",methods=["GET","POST"])
@require_role(CrewPermissions.removeMemberRole)
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    form = RemoveCrewMemberForm()
    crew = list()
    if request.method == 'GET':
        try:
            with db.bind.Session() as s:
                with s.begin():
                    crew = s.scalars(selectCrew()).all()
        except Exception as e:
            return await render_template("error.html",sectionName,error="GET: "+str(e))
        form.Nickname.choices = [(c.Nickname,c.Nickname) for c in crew]
        return await render_template("crewMemberRemove.html",sectionName,FORM=form)
    elif request.method == 'POST':
        members = (await request.form).getlist('Nickname')
        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        for member in members:
                            personId     = (s.scalar(selectPerson(member))).Id
                            memberSerial = (s.execute(selectCrew(member)).first())[3]
                            s.query(CrewMemberDivisionTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberRankTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberTable).filter_by(PersonalBaseInformationsId=personId).delete()
                            s.query(PersonalBaseInformationsTable).filter_by(Nickname=member).delete()
                        s.commit()
                        s.flush()
            except Exception as e:
                return await render_template("error.html",sectionName,error="1: "+str(e))
        return redirect(url_for('crew.remove'))
    else:
        return await render_template("error.html",sectionName,error="Invalid method")

@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
@require_role(CrewPermissions.editMemberRole)
async def edit(member):
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    form         = EditCrewMemberForm()
    ranks        = []
    duties       = []
    divisions    = []

    memberSerial             = 0
    personId                 = 0
    personalBaseInformations = PersonalBaseInformationsTable()
    crewMember               = CrewMemberTable()
    crewMemberRank           = CrewMemberRankTable()
    crewMemberDivision       = CrewMemberDivisionTable()
    crewMemberDuties         = []

    if request.method == 'GET':
        try:
            with db.bind.Session() as s:
                with s.begin():
                    crewMember               = s.execute(selectCrew(member)).all()
                    ranks                    = s.scalars(selectRank()).all()
                    duties                   = s.scalars(selectDuty()).all()
                    divisions                = s.scalars(selectDivision()).all()

                    personId                 = (s.scalar(selectPerson(member))).Id
                    memberSerial             = (s.execute(selectCrew(member)).first())[3]
                    personalBaseInformations = s.query(PersonalBaseInformationsTable)\
                                                .filter_by(Id=personId).first()
                    crewMember               = s.query(CrewMemberTable)\
                                                .filter_by(Serial=memberSerial).first()
                    crewMemberRank           = s.query(CrewMemberRankTable)\
                                                .filter_by(MemberSerial=memberSerial).first()
                    crewMemberDivision       = s.query(CrewMemberDivisionTable)\
                                                .filter_by(MemberSerial=memberSerial).first()
                    crewMemberDuties         = s.query(CrewMemberDutyTable)\
                                                .filter_by(MemberSerial=memberSerial).all()
        except Exception as e:
            return await render_template("error.html",sectionName,error="GET: "+str(e))
        form.FirstName.data   = personalBaseInformations.FirstName
        form.LastName.data    = personalBaseInformations.LastName
        form.Nickname.data    = personalBaseInformations.Nickname
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Rank.default     = crewMemberRank.RankName
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        form.Division.default = crewMemberDivision.DivisionName
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Duties.default   = [(d.DutyName,d.DutyName) for d in crewMemberDuties]
        return await render_template("crewMemberEdit.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            firstname      = (await request.form)['FirstName']
            lastname       = (await request.form)['LastName']
            nickname       = (await request.form)['Nickname']
            rank           = (await request.form)['Rank']
            division       = (await request.form)['Division']
            selectedDuties = (await request.form).getlist('Duties')

            dutyAlreadyPresent = False
            dutyRemoved        = False
            dutyIndex          = 0

            try:
                with db.bind.Session() as s:
                    with s.begin():
                        crewMember               = s.execute(selectCrew(member)).all()
                        ranks                    = s.scalars(selectRank()).all()
                        duties                   = s.scalars(selectDuty()).all()
                        divisions                = s.scalars(selectDivision()).all()

                        personId                 = (s.scalar(selectPerson(member))).Id
                        memberSerial             = (s.execute(selectCrew(member)).first())[3]
                        personalBaseInformations = s.query(PersonalBaseInformationsTable)\
                                                    .filter_by(Id=personId).update({'FirstName':firstname,'LastName':lastname,'Nickname':nickname})
                        crewMember               = s.query(CrewMemberTable)\
                                                    .filter_by(Serial=memberSerial).first()
                        crewMemberRank           = s.query(CrewMemberRankTable)\
                                                    .filter_by(MemberSerial=memberSerial).update({'RankName': rank})
                        crewMemberDivision       = s.query(CrewMemberDivisionTable)\
                                                    .filter_by(MemberSerial=memberSerial).update({'DivisionName': division})
                        crewMemberDuties         = s.query(CrewMemberDutyTable)\
                                                    .filter_by(MemberSerial=memberSerial).all()
            except Exception as e:
                return await render_template("error.html",sectionName,error="1: "+str(e))
            if len(selectedDuties):
                try:
                    with db.bind.Session() as s:
                        with s.begin():
                            for newDuty in selectedDuties:
                                for oldDuty in crewMemberDuties:
                                    if newDuty == oldDuty.DutyName:
                                        dutyAlreadyPresent = True
                                        break
                                if not dutyAlreadyPresent:
                                    newDuty            = CrewMemberDutyTable(MemberSerial=memberSerial,
                                                                            DutyName=newDuty)
                                    s.add(newDuty)
                                dutyAlreadyPresent = False
                            s.commit()
                            s.flush()
                except Exception as e:
                    return await render_template("error.html",sectionName,error="2: "+str(e))
                try:
                    with db.bind.Session() as s:
                        with s.begin():
                            for oldDuty in crewMemberDuties:
                                for newDuty in selectedDuties:
                                    if newDuty == oldDuty.DutyName:
                                        dutyAlreadyPresent = True
                                        break
                                if not dutyAlreadyPresent:
                                    removeDuty = s.query(CrewMemberDutyTable)\
                                                .filter(and_(CrewMemberDutyTable.MemberSerial==memberSerial,
                                                            CrewMemberDutyTable.DutyName==oldDuty.DutyName))\
                                                .delete()
                                dutyAlreadyPresent = False
                            s.commit()
                            s.flush()
                except Exception as e:
                    return await render_template("error.html",sectionName,error="3: "+str(e))
            return redirect(url_for('crew.edit',member=personalBaseInformations.Nickname))
    else:
        return await render_template("error.html",sectionName,error="Invalid method")
