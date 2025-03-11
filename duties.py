from quart          import Blueprint,current_app,request,render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,DutyTable
from forms import AddDutyForm,RemoveDutyForm,EditDutyForm

duties_blueprint = Blueprint("duties",__name__,url_prefix='/duties',template_folder='templates/default')

class Duty:
    def __init__(self):
        self.name        = ""
        self.description = ""

    async def edit(self,name,description) -> bool:
        pass


class DutyList:
    def __init__(self):
        self.Duty = list()

    async def add(self,duty:Duty) -> bool:
        pass
    async def remove(self,duty:Duty) -> bool:
        pass

@duties_blueprint.route("/",methods=["GET"])
async def view():
    return "Implement!"

@duties_blueprint.route("/duty/<duty>",methods=["GET"])
async def duty(duty):
    return "Implement!"

@duties_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form = AddDutyForm()
    if request.method == 'GET':
        return await render_template("dutyAdd.html",FORM=form,SECTIONNAME="Duties")
    elif request.method == 'POST':
        name         = (await request.form)['Name']
        description  = (await request.form)['Description']
        duty         = DutyTable(Name=name,Description=description)
        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(duty)
                        s.commit()
            except Exception as e:
                return await render_template("dutyAdd.html",FORM=form,SECTIONNAME="Duties",MESSAGE=str(e))
            return await render_template("dutyAdd.html",FORM=form,SECTIONNAME="Duties",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Duties")

@duties_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    form = RemoveDutiesForm()
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Duties")

@duties_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return "Implement!"
