from quart          import Blueprint,current_app,render_template,request
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,PersonalBaseInformationsTable,CrewMemberTable,RankTable,DutyTable,MemberOnboardLogEntryTable,MemberRankLogEntryTable,MemberDivisionLogEntryTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable
from forms import AddCrewMemberForm,RemoveCrewMemberForm,EditCrewMemberForm

divisions_blueprint = Blueprint("divisions",__name__,url_prefix='/divisions',template_folder='templates/default')

@divisions_blueprint.route("/",methods=["GET"])
async def divisions():
    divisions = list()
    with db.bind.Session() as s:
        with s.begin():
            divisions = s.query(select(DivisionTable.Nickname).distinct(DivisionTable.Nickname).subquery()).all()
    if len(divisions) > 0:
        return await render_template("divisions.html",divisions=divisions,SECTIONNAME="Divisions")
    else:
        return await render_template("divisions.html",divisions=str("No divisions found"),SECTIONNAME="Divisions")

@divisions_blueprint.route("/division/<division>",methods=["GET"])
async def division(division):
    return "Implement!"

@divisions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form   = AddDivisionForm()
    if request.method == 'GET':
        return await render_template("crewMemberAdd.html",FORM=form,SECTIONNAME="Crew")
    elif request.method == 'POST':
        name        = (await request.form)['Name']
        description = (await request.form)['Description']

        division = DivisionTable(Name=name,Description=description)

        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(division)
                        s.commit()
            except Exception as e:
                return await render_template("divisionsAdd.html",FORM=form,SECTIONNAME="Divisions",MESSAGE=str(e))
            return await render_template("divisionsAdd.html",FORM=form,SECTIONNAME="Divisions",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Divisions")

@divisions_blueprint.route("/remove/<division>",methods=["GET","POST"])
async def remove(division):
    return "Implement!"

@divisions_blueprint.route("/edit/<division>",methods=["GET","POST"])
async def edit(division):
    return "Implement!"
