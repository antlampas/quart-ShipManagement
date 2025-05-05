from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from authorization  import require_role

from model          import db
from model          import CrewMemberTable
from model          import DutyTable

from forms          import AddDutyForm
from forms          import RemoveDutyForm
from forms          import EditDutyForm

duties_blueprint = Blueprint("duties",__name__,url_prefix='/duties',template_folder='templates/default')

addDutyRole    = ""
removeDutyRole = ""
editDutyRole   = ""

@duties_blueprint.route("/",methods=["GET"])
async def view():
    return "Implement!"

@duties_blueprint.route("/duty/<duty>",methods=["GET"])
async def duty(duty):
    return "Implement!"

@duties_blueprint.route("/add",methods=["GET","POST"])
@require_role(addDutyRole)
async def add():
    form = AddDutyForm()
    if request.method == 'GET':
        return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME="Duties")
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
                return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME="Duties",MESSAGE=str(e))
            return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME="Duties",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Duties")

@duties_blueprint.route("/remove",methods=["GET","POST"])
@require_role(removeDutyRole)
async def remove():
    form = RemoveDutiesForm()
    return await render_template("implement.html",implement="Implement!",SECTIONNAME="Duties")

@duties_blueprint.route("/edit",methods=["GET","POST"])
@require_role(editDutyRole)
async def edit():
    return "Implement!"
