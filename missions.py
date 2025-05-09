from quart import Blueprint
from quart import current_app
from quart import render_template
from quart import request

from model import db
from model import CrewMemberTable
from model import TaskTable
from model import MissionTable
from model import MemberTaskLogEntryTable
from model import MemberMissionLogEntryTable

from authorization  import require_role
from authorization  import require_login

from permissions    import CrewOnBoardLogPermissions

from baseClasses    import Editable
from baseClasses    import Addable

from standardReturn import standardReturn

missions_blueprint = Blueprint("missions",__name__,url_prefix='/missions',template_folder='templates/default')

sectionName = "Missions"

@missions_blueprint.route("/",methods=["GET"])
async def missions():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/mission/<mission>",methods=["GET"])
@require_login
async def view(mission):
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/add",methods=["GET","POST"])
@require_role(MissionsPermissions.addMissionRole)
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/remove",methods=["GET","POST"])
@require_role(MissionsPermissions.removeMissionRole)
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/edit",methods=["GET","POST"])
@require_role(MissionsPermissions.editMissionRole)
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
