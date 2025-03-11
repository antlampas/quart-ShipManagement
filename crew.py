from quart          import Blueprint,current_app,render_template,request
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,MemberOnboardLogEntryTable,MemberRankLogEntryTable,MemberDivisionLogEntryTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable
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
            crewMemberQuery = s.query(select(CrewMemberTable.Nickname).distinct(CrewMemberTable.Nickname).where(CrewMemberTable.Nickname==member).subquery()).one()

    if len(crewMember) > 0:
        crewMember = CrewMember()
        crewMember.FirstName = crewMemberQuery[0]
        crewMember.LastName  = crewMemberQuery[1]
        crewMember.Nickname  = crewMemberQuery[2]
        #TODO: complete the query and the object with Rank and Duties
        return await render_template("crewMember.html",crewMember=crewMember,SECTIONNAME="Crew")
    else:
        return await render_template("crewMember.html",crewMember=str("No crew member found"),SECTIONNAME="Crew")

@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form = AddCrewMemberForm()
    if request.method == 'GET':
        return await render_template("crewMemberAdd.html",SECTIONNAME="Crew")
    elif request.method == 'POST':
        return await render_template("crewMemberAdd.html",SECTIONNAME="Crew")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Crew")

@crew_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    form = RemoveCrewMemberForm()
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Crew")

@crew_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    form = EditCrewMemberForm()
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Crew")
