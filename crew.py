from quart          import Blueprint,current_app,render_template,request
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,PersonalBaseInformationsTable,CrewMemberTable,RankTable,DutyTable,DivisionTable,CrewMemberRankTable,CrewMemberDutyTable,CrewMemberDivisionTable,MemberOnboardLogEntryTable,MemberRankLogEntryTable,MemberDivisionLogEntryTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable,selectCrew,selectRank,selectDuties,selectDivision
from forms import AddCrewMemberForm,RemoveCrewMemberForm,EditCrewMemberForm

crew_blueprint = Blueprint("crew",__name__,url_prefix='/crew',template_folder='templates/default')

@crew_blueprint.route("/",methods=["GET"])
async def crew():
    crew = list()
    with db.bind.Session() as s:
        with s.begin():
            crew = s.query(selectCrew()).all()
    if len(crew) > 0:
        return await render_template("crew.html",crew=crew,SECTIONNAME="Crew")
    else:
        return await render_template("crew.html",crew=str("No crew member found"),SECTIONNAME="Crew")

@crew_blueprint.route("/member/<member>",methods=["GET"])
async def member(member):
    crewMember = CrewMember()
    try:
        with db.bind.Session() as s:
            with s.begin():
                crewMember = s.scalar(selectCrew(member).order_by(CrewMemberTable.Nickname)).one()
    except Exception as e:
        return await render_template("crewMember.html",crewMember=str("No crew member found with that name"),SECTIONNAME="Crew")
    return await render_template("crewMember.html",crewMember=crewMember,SECTIONNAME="Crew")

@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
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
                return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew",MESSAGE=str(e))
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew")
    elif request.method == 'POST':
        firstname = (await request.form)['FirstName']
        lastname  = (await request.form)['LastName']
        nickname  = (await request.form)['Nickname']
        rank      = (await request.form)['Rank']
        duties    = (await request.form)['Duties']
        division  = (await request.form)['Division']

        personalBaseInformations = PersonalBaseInformationsTable(FirstName=firstname,LastName=lastname,Nickname=nickname)
        crewMember               = CrewMemberTable(Nickname=nickname)
        crewMemberRank           = CrewMemberRankTable(CrewMember=nickname,Rank=rank)
        crewMemberDuties         = CrewMemberDutyTable(CrewMember=nickname,Duty=duties)
        crewMemberDivision       = CrewMemberDivisionTable(CrewMember=nickname,Division=division)

        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(personalBaseInformations)
                        s.add(crewMember)
                        s.add(crewMemberRank)
                        s.add(crewMemberDuties)
                        s.add(crewMemberDivision)
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
    crewMemberDB = CrewMemberTable()
    if request.method == 'GET':
        with db.bind.Session() as s:
            with s.begin():
                crewMemberDB = s.scalar(selectCrew(member)).one()
        form.FirstName.data = crewMemberDB.FirstName
        form.LastName.data  = crewMemberDB.LastName
        form.Nickname.data  = crewMemberDB.Nickname
        form.Rank.data      = crewMemberDB.Rank
        form.Division.data  = crewMemberDB.Division
        form.Duties.data    = crewMemberDB.Duties
        return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew")
    elif request.method == 'POST':
        firstname = (await request.form)['FirstName']
        lastname  = (await request.form)['LastName']
        nickname  = (await request.form)['Nickname']
        rank      = (await request.form)['Rank']
        duties    = (await request.form)['Duties']
        division  = (await request.form)['Division']

        personalBaseInformations = PersonalBaseInformationsTable(FirstName=firstname,LastName=lastname,Nickname=nickname)
        crewMember               = CrewMemberTable(Nickname=nickname)
        crewMemberRank           = CrewMemberRankTable(CrewMember=nickname,Rank=rank)
        crewMemberDuties         = CrewMemberDutyTable(CrewMember=nickname,Duty=duties)
        crewMemberDivision       = CrewMemberDivisionTable(CrewMember=nickname,Division=division)

        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.edit(personalBaseInformations)
                        s.edit(crewMember)
                        s.edit(crewMemberRank)
                        s.edit(crewMemberDuties)
                        s.edit(crewMemberDivision)
                        s.commit()
            except:
                return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew",MESSAGE="Exception!")
            return await render_template("crewMemberEdit.html",FORM=form,SECTIONNAME="Crew",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Crew")
