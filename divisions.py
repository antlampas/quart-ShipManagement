from quart          import Blueprint,current_app,render_template,request,redirect
from sqlalchemy     import select
from sqlalchemy.orm import Session

from time           import sleep

from model          import db,DivisionTable,selectDivision
from forms          import AddDivisionForm,RemoveDivisionForm,EditDivisionForm

divisions_blueprint = Blueprint("divisions",__name__,url_prefix='/divisions',template_folder='templates/default')

@divisions_blueprint.route("/",methods=["GET"])
async def divisions():
    divisions = list()
    with db.bind.Session() as s:
        with s.begin():
            divisions = s.scalars(selectDivision()).all()
    if len(divisions) > 0:
        return await render_template("divisions.html",divisions=divisions,SECTIONNAME="Divisions")
    else:
        return await render_template("divisions.html",divisions=str("No divisions found"),SECTIONNAME="Divisions")

@divisions_blueprint.route("/division/<division>",methods=["GET"])
async def division(division):
    return "Implement!"

@divisions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form = AddDivisionForm()
    if request.method == 'GET':
        return await render_template("divisionsAdd.html",FORM=form,SECTIONNAME="Crew")
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

@divisions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    form = RemoveDivisionForm()
    divisions = list()
    if request.method == 'GET':
        try:
            with db.bind.Session() as s:
                with s.begin():
                    divisions = s.scalars(selectDivision()).all()
        except Exception as e:
            return await render_template("divisionsRemove.html",FORM=form,SECTIONNAME="Divisions",MESSAGE=str(e))
        form.Name.choices = [(d.Name,d.Name) for d in divisions]
        return await render_template("divisionsRemove.html",FORM=form,SECTIONNAME="Divisions")
    elif request.method == 'POST':
        if form.validate_on_submit():
            division = (await request.form).getlist('Name')
            try:
                for i in division:
                    with db.bind.Session() as s:
                        with s.begin():
                            d = s.scalar(selectDivision(i))
                            s.delete(d)
                            s.commit()
            except Exception as e:
                return await render_template("divisionsRemove.html",FORM=form,SECTIONNAME="Divisions",MESSAGE="1: "+str(e))
            form = RemoveDivisionForm()
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        d = s.scalars(selectDivision()).all()
                        for i in d:
                            divisions = s.scalars(selectDivision()).all()
            except Exception as e:
                return await render_template("divisionsRemove.html",FORM=form,SECTIONNAME="Divisions",MESSAGE="2: "+str(e))
            form.Name.choices = [(d.Name,d.Name) for d in divisions]
            return await render_template("divisionsRemove.html",FORM=form,SECTIONNAME="Divisions",MESSAGE="Success")
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Division")

@divisions_blueprint.route("/edit/<division>",methods=["GET","POST"])
async def edit(division):
    return "Implement!"
