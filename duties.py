from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import DutyTable

from forms          import AddDutyForm
from forms          import RemoveDutyForm
from forms          import EditDutyForm

from authorization  import require_role
from authorization  import require_login
from permissions    import DutiesPermissions
from standardReturn import standardReturn
duties_blueprint = Blueprint("duties",__name__,url_prefix='/duties',template_folder='templates/default')

sectionName = "Duties"

@duties_blueprint.route("/duty/<duty>",methods=["GET"])
@require_login
async def duty(duty):
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")

@duties_blueprint.route("/add",methods=["GET","POST"])
@require_role(DutiesPermissions.addDutyRole)
async def add():
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form = AddDutyForm()
    # if request.method == 'GET':
    #     return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME=sectionName)
    # elif request.method == 'POST':
    #     name         = (await request.form)['Name']
    #     description  = (await request.form)['Description']
    #     duty         = DutyTable(Name=name,Description=description)
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     s.add(duty)
    #                     s.commit()
    #         except Exception as e:
    #             return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME=sectionName,MESSAGE=str(e))
    #         return await render_template("dutiesAdd.html",FORM=form,SECTIONNAME=sectionName,MESSAGE="Success")
    # else:
    #     return await render_template("error.html",error="Invalid method",SECTIONNAME=sectionName)

@duties_blueprint.route("/remove",methods=["GET","POST"])
@require_role(DutiesPermissions.removeDutyRole)
async def remove():
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack

@duties_blueprint.route("/edit",methods=["GET","POST"])
@require_role(DutiesPermissions.editDutyRole)
async def edit():
    return await standardReturn("implement.html",SECTIONNAME=sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
