from quart          import Blueprint,current_app,render_template,request
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,PersonalBaseInformationsTable,CrewMemberTable,RankTable,DutyTable,MemberOnboardLogEntryTable,MemberRankLogEntryTable,MemberDivisionLogEntryTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable
from forms import AddCrewMemberForm,RemoveCrewMemberForm,EditCrewMemberForm

crew_blueprint = Blueprint("crew",__name__,url_prefix='/crew',template_folder='templates/default')

class CrewMember:
    def __init__(self):
        self.FirstName = ""
        self.LastName  = ""
        self.Nickname  = ""
        self.Rank      = ""
        self.Division  = ""
        self.Duties    = ""

    async def edit(self,firstName,lastName,nickname,rank,division,duties) -> bool:
        pass

class Crew:
    def __init__(self):
        self.CrewMember = list()

    async def add(self,member:CrewMember) -> bool:
        pass
    async def remove(self,member:CrewMember) -> bool:
        pass

@crew_blueprint.route("/",methods=["GET"])
async def crew():
    crew = list()
    with db.bind.Session() as s:
        with s.begin():
            crew = s.query(select(CrewMemberTable.Nickname).distinct(CrewMemberTable.Nickname).subquery()).all()
    if len(crew) > 0:
        return await render_template("crew.html",crew=crew,SECTIONNAME="Crew")
    else:
        return await render_template("crew.html",crew=str("No crew member found"),SECTIONNAME="Crew")

@crew_blueprint.route("/member/<member>",methods=["GET"])
async def member(member):
    crewMemberQuery = list()
    with db.bind.Session() as s:
        with s.begin():
            #crewMemberQuery = s.query(select(CrewMemberTable.Nickname).distinct(CrewMemberTable.Nickname).where(CrewMemberTable.Nickname==member).subquery()).one()
            crewMemberQuery = s.query(select(PersonalBaseInformationsTable.Nickname).distinct(PersonalBaseInformationsTable.Nickname).where(PersonalBaseInformationsTable.Nickname==member).subquery()).one()
    if len(crewMember) > 0:
        crewMember = CrewMember(FirstName=crewMemberQuery[0],LastName=crewMemberQuery[1],Nickname=crewMemberQuery[2])
        #TODO: complete the query and the object with Rank and Duties
        return await render_template("crewMember.html",crewMember=crewMember,SECTIONNAME="Crew")
    else:
        return await render_template("crewMember.html",crewMember=str("No crew member found"),SECTIONNAME="Crew")

@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form   = AddCrewMemberForm()
    if request.method == 'GET':
        ranks  = []
        duties = []
        try:
            with db.bind.Session() as s:
                with s.begin():
                    ranks  = s.scalars(select(RankTable.Name)).all()
                    duties = s.scalars(select(DutyTable.Name)).all()
        except Exception as e:
                return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew",MESSAGE=str(e))
        form.Rank.choices = [(r,r) for r in ranks]
        form.Duties.choices = [(d,d) for d in duties]
        return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew")
    elif request.method == 'POST':
        firstname = (await request.form)['FirstName']
        lastname  = (await request.form)['LastName']
        nickname  = (await request.form)['Nickname']
        rank      = (await request.form)['Rank']
        duties    = (await request.form)['Duties']

        personalBaseInformations = PersonalBaseInformationsTable(FirstName=firstname,LastName=lastname,Nickname=nickname)
        crewMemberRank           = CrewMembeRankrTable(Nickname=nickname,Rank=rank)
        crewMemberDuties         = CrewMemberDutyTable(Nickname=nickname,Rank=rank,Duties=duties)

        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(personalBaseInformations)
                        #s.add(crewMember)
                        s.commit()
            except Exception as e:
                return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew",MESSAGE=str(e))
            return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Crew")

@crew_blueprint.route("/remove/<member>",methods=["GET","POST"])
async def remove(member):
    form = RemoveCrewMemberForm()
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Crew")

@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
async def edit(member):
    #TODO: Fix this function
    form = EditCrewMemberForm()
    crewMemberDB = ""
    if request.method == 'GET':
        with db.bind.Session() as s:
            with s.begin():
                #crewMemberDB = s.query(CrewMemberTable).filter_by(Nickname=member).one()
                crewMemberDB = s.query(PersonalBaseInformationsTable).filter_by(Nickname=member).one()
        form.FirstName.data = crewMemberDB.FirstName
        form.LastName.data  = crewMemberDB.LastName
        form.Nickname.data  = crewMemberDB.Nickname
        return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew")
    elif request.method == 'POST':
        firstname = (await request.form)['FirstName']
        lastname  = (await request.form)['LastName']
        nickname  = (await request.form)['Nickname']
        #crewMember = CrewMemberTable(FirstName=request.form['FirstName'],LastName=request.form['LastName'],Nickname=request.form['Nickname'])
        crewMember = PersonalBaseInformationsTable(FirstName=firstname,LastName=lastname,Nickname=nickname)
        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.edit(crewMember)
                        s.commit()
            except:
                return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew",MESSAGE="Exception!")
            return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Crew")
