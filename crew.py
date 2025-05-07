from quart          import Blueprint
from quart          import current_app
from quart          import render_template
from quart          import request
from quart          import redirect
from quart          import url_for
from quart          import session
from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from types          import SimpleNamespace
from time           import sleep
from jose           import jwt

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
from baseClasses    import Editable,Addable
from standardReturn import standardReturn

crew_blueprint = Blueprint("crew",__name__,url_prefix='/crew',template_folder='templates/default')

sectionName = "Crew"

class CrewMember(Editable):
    def __init__(self,FirstName,LastName,Nickname,Rank,Division,Duties:list()):
        self.FirstName = FirstName
        self.LastName  = LastName
        self.Nickname  = Nickname
        self.Rank      = Rank
        self.Division  = Division
        self.Duties    = Duties
    def edit(self,attributes:dict):
        pass

class Crew(Addable):
    def __init__(self,member:CrewMember):
        self.crew = crew
    def add(self,member:CrewMember):
        pass
    def remove(self,member:CrewMember):
        pass

@crew_blueprint.route("/",methods=["GET"])
@require_login
async def crew():
    crew = list()
    with db.bind.Session() as s:
        with s.begin():
            crew = s.scalars(selectCrew()).all()
    if len(crew) > 0:
        return await standardReturn("crew.html",SECTIONNAME=sectionName,crew=crew)
    else:
        return await standardReturn("error.html",SECTIONNAME=sectionName,error="No crew member found")

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
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form   = AddCrewMemberForm()
    # if request.method == 'GET':
    #     ranks     = []
    #     duties    = []
    #     divisions = []
    #     try:
    #         with db.bind.Session() as s:
    #             with s.begin():
    #                 ranks     = s.scalars(selectRank()).all()
    #                 duties    = s.scalars(selectDuty()).all()
    #                 divisions = s.scalars(selectDivision()).all()
    #     except Exception as e:
    #             return await render_template("error.html",error=str(e),SECTIONNAME=sectionName)
    #     form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
    #     form.Duties.choices   = [(d.Name,d.Name) for d in duties]
    #     form.Division.choices = [(d.Name,d.Name) for d in divisions]
    #     return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME=sectionName)
    # elif request.method == 'POST':
    #     firstname = (await request.form)['FirstName']
    #     lastname  = (await request.form)['LastName']
    #     nickname  = (await request.form)['Nickname']
    #     rank      = (await request.form)['Rank']
    #     duties    = (await request.form).getlist('Duties')
    #     division  = (await request.form)['Division']
    #
    #     personalBaseInformations = PersonalBaseInformationsTable(FirstName=firstname,
    #                                                             LastName=lastname,
    #                                                             Nickname=nickname)
    #     person     = PersonalBaseInformationsTable()
    #     crewMember = CrewMemberTable()
    #
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     s.add(personalBaseInformations)
    #                     s.commit()
    #                     s.flush()
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     person     = s.scalar(selectPerson(nickname))
    #                     crewMember = CrewMemberTable(PersonalBaseInformationsId=person.Id)
    #                     s.add(crewMember)
    #                     s.commit()
    #                     s.flush()
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     person             = s.scalar(selectPerson(nickname))
    #                     crewMember         = s.scalar(select(CrewMemberTable)\
    #                                         .where(CrewMemberTable.PersonalBaseInformationsId==person.Id))
    #                     crewMemberRank     = CrewMemberRankTable(MemberSerial=crewMember.Serial,
    #                                                             RankName=rank)
    #                     crewMemberDivision = CrewMemberDivisionTable(MemberSerial=crewMember.Serial,
    #                                                                 DivisionName=division)
    #                     s.add(crewMemberRank)
    #                     s.add(crewMemberDivision)
    #                     s.commit()
    #                     s.flush()
    #             for duty in duties:
    #                 with db.bind.Session() as s:
    #                     with s.begin():
    #                         person         = s.scalar(selectPerson(nickname))
    #                         crewMember     = s.scalar(select(CrewMemberTable)\
    #                                         .where(CrewMemberTable.PersonalBaseInformationsId==person.Id))
    #                         crewMemberDuty = CrewMemberDutyTable(MemberSerial=crewMember.Serial,
    #                                         DutyName=duty)
    #                         s.add(crewMemberDuty)
    #                         s.commit()
    #                         s.flush()
    #         except Exception as e:
    #             return await render_template("error.html",error="1: "+str(e),SECTIONNAME=sectionName)
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     ranks     = s.scalars(selectRank()).all()
    #                     duties    = s.scalars(selectDuty()).all()
    #                     divisions = s.scalars(selectDivision()).all()
    #         except Exception as e:
    #                 return await render_template("error.html",error="2: "+str(e),SECTIONNAME=sectionName)
    #         form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
    #         form.Duties.choices   = [(d.Name,d.Name) for d in duties]
    #         form.Division.choices = [(d.Name,d.Name) for d in divisions]
    #         return await render_template("crewMemberAdd.html",
    #                                     FORM=form,
    #                                     DUTIES=duties,
    #                                     SECTIONNAME=sectionName,
    #                                     MESSAGE='Success')
    # else:
    #     return await render_template("error.html",error="Invalid method",SECTIONNAME=sectionName)

@crew_blueprint.route("/remove",methods=["GET","POST"])
@require_role(CrewPermissions.removeMemberRole)
async def remove():
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form = RemoveCrewMemberForm()
    # crew = list()
    # if request.method == 'GET':
    #     try:
    #         with db.bind.Session() as s:
    #             with s.begin():
    #                 crew = s.scalars(selectCrew()).all()
    #     except Exception as e:
    #         return await render_template("error.html",error="GET: "+str(e),SECTIONNAME=sectionName)
    #     form.Nickname.choices = [(c.Nickname,c.Nickname) for c in crew]
    #     return await render_template("crewMemberRemove.html",FORM=form,SECTIONNAME=sectionName)
    # elif request.method == 'POST':
    #     members = (await request.form).getlist('Nickname')
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     for member in members:
    #                         personId     = (s.scalar(selectPerson(member))).Id
    #                         memberSerial = (s.execute(selectCrew(member)).first())[3]
    #                         s.query(CrewMemberDivisionTable).filter_by(MemberSerial=memberSerial).delete()
    #                         s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).delete()
    #                         s.query(CrewMemberRankTable).filter_by(MemberSerial=memberSerial).delete()
    #                         s.query(CrewMemberTable).filter_by(PersonalBaseInformationsId=personId).delete()
    #                         s.query(PersonalBaseInformationsTable).filter_by(Nickname=member).delete()
    #                     s.commit()
    #                     s.flush()
    #         except Exception as e:
    #             return await render_template("error.html",error="1: "+str(e),SECTIONNAME=sectionName)
    #     return redirect(url_for('crew.remove'))
    # else:
    #     return await render_template("error.html",error="Invalid method",SECTIONNAME=sectionName)

@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
@require_role(CrewPermissions.editMemberRole)
async def edit(member):
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form         = EditCrewMemberForm()
    # ranks        = []
    # duties       = []
    # divisions    = []
    #
    # memberSerial             = 0
    # personId                 = 0
    # personalBaseInformations = PersonalBaseInformationsTable()
    # crewMember               = CrewMemberTable()
    # crewMemberRank           = CrewMemberRankTable()
    # crewMemberDivision       = CrewMemberDivisionTable()
    # crewMemberDuties         = []
    #
    # if request.method == 'GET':
    #     try:
    #         with db.bind.Session() as s:
    #             with s.begin():
    #                 crewMember               = s.execute(selectCrew(member)).all()
    #                 ranks                    = s.scalars(selectRank()).all()
    #                 duties                   = s.scalars(selectDuty()).all()
    #                 divisions                = s.scalars(selectDivision()).all()
    #
    #                 personId                 = (s.scalar(selectPerson(member))).Id
    #                 memberSerial             = (s.execute(selectCrew(member)).first())[3]
    #                 personalBaseInformations = s.query(PersonalBaseInformationsTable)\
    #                                             .filter_by(Id=personId).first()
    #                 crewMember               = s.query(CrewMemberTable)\
    #                                             .filter_by(Serial=memberSerial).first()
    #                 crewMemberRank           = s.query(CrewMemberRankTable)\
    #                                             .filter_by(MemberSerial=memberSerial).first()
    #                 crewMemberDivision       = s.query(CrewMemberDivisionTable)\
    #                                             .filter_by(MemberSerial=memberSerial).first()
    #                 crewMemberDuties         = s.query(CrewMemberDutyTable)\
    #                                             .filter_by(MemberSerial=memberSerial).all()
    #     except Exception as e:
    #         return await render_template("error.html",error="GET: "+str(e),SECTIONNAME=sectionName)
    #     form.FirstName.data   = personalBaseInformations.FirstName
    #     form.LastName.data    = personalBaseInformations.LastName
    #     form.Nickname.data    = personalBaseInformations.Nickname
    #     form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
    #     form.Rank.default     = crewMemberRank.RankName
    #     form.Division.choices = [(d.Name,d.Name) for d in divisions]
    #     form.Division.default = crewMemberDivision.DivisionName
    #     form.Duties.choices   = [(d.Name,d.Name) for d in duties]
    #     form.Duties.default   = [(d.DutyName,d.DutyName) for d in crewMemberDuties]
    #     return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME=sectionName)
    # elif request.method == 'POST':
    #     if form.validate_on_submit():
    #         firstname      = (await request.form)['FirstName']
    #         lastname       = (await request.form)['LastName']
    #         nickname       = (await request.form)['Nickname']
    #         rank           = (await request.form)['Rank']
    #         division       = (await request.form)['Division']
    #         selectedDuties = (await request.form).getlist('Duties')
    #
    #         dutyAlreadyPresent = False
    #         dutyRemoved        = False
    #         dutyIndex          = 0
    #
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     crewMember               = s.execute(selectCrew(member)).all()
    #                     ranks                    = s.scalars(selectRank()).all()
    #                     duties                   = s.scalars(selectDuty()).all()
    #                     divisions                = s.scalars(selectDivision()).all()
    #
    #                     personId                 = (s.scalar(selectPerson(member))).Id
    #                     memberSerial             = (s.execute(selectCrew(member)).first())[3]
    #                     personalBaseInformations = s.query(PersonalBaseInformationsTable)\
    #                                                 .filter_by(Id=personId).update({'FirstName':firstname,'LastName':lastname,'Nickname':nickname})
    #                     crewMember               = s.query(CrewMemberTable)\
    #                                                 .filter_by(Serial=memberSerial).first()
    #                     crewMemberRank           = s.query(CrewMemberRankTable)\
    #                                                 .filter_by(MemberSerial=memberSerial).update({'RankName': rank})
    #                     crewMemberDivision       = s.query(CrewMemberDivisionTable)\
    #                                                 .filter_by(MemberSerial=memberSerial).update({'DivisionName': division})
    #                     crewMemberDuties         = s.query(CrewMemberDutyTable)\
    #                                                 .filter_by(MemberSerial=memberSerial).all()
    #         except Exception as e:
    #             return await render_template("error.html",error="1: "+str(e),SECTIONNAME=sectionName)
    #         if len(selectedDuties):
    #             try:
    #                 with db.bind.Session() as s:
    #                     with s.begin():
    #                         for newDuty in selectedDuties:
    #                             for oldDuty in crewMemberDuties:
    #                                 if newDuty == oldDuty.DutyName:
    #                                     dutyAlreadyPresent = True
    #                                     break
    #                             if not dutyAlreadyPresent:
    #                                 newDuty            = CrewMemberDutyTable(MemberSerial=memberSerial,
    #                                                                         DutyName=newDuty)
    #                                 s.add(newDuty)
    #                             dutyAlreadyPresent = False
    #                         s.commit()
    #                         s.flush()
    #             except Exception as e:
    #                 return await render_template("error.html",error="2: "+str(e),SECTIONNAME=sectionName)
    #             try:
    #                 with db.bind.Session() as s:
    #                     with s.begin():
    #                         for oldDuty in crewMemberDuties:
    #                             for newDuty in selectedDuties:
    #                                 if newDuty == oldDuty.DutyName:
    #                                     dutyAlreadyPresent = True
    #                                     break
    #                             if not dutyAlreadyPresent:
    #                                 removeDuty = s.query(CrewMemberDutyTable)\
    #                                             .filter(and_(CrewMemberDutyTable.MemberSerial==memberSerial,
    #                                                         CrewMemberDutyTable.DutyName==oldDuty.DutyName))\
    #                                             .delete()
    #                             dutyAlreadyPresent = False
    #                         s.commit()
    #                         s.flush()
    #             except Exception as e:
    #                 return await render_template("error.html",error="3: "+str(e),SECTIONNAME=sectionName)
    #         return redirect(url_for('crew.edit',member=personalBaseInformations.Nickname))
    # else:
    #     return await render_template("error.html",error="Invalid method",SECTIONNAME=sectionName)
