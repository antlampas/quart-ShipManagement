from quart import Blueprint
from quart import current_app

from authorization  import require_role

from model import db
from model import CrewMemberTable
from model import TaskTable
from model import MissionTable
from model import MemberTaskLogEntryTable
from model import MemberMissionLogEntryTable

missions_blueprint = Blueprint("missions",__name__,url_prefix='/missions',template_folder='templates/default')

addMissionRole    = ""
removeMissionRole = ""
editMissionRole   = ""

@missions_blueprint.route("/mission/<mission>",methods=["GET"])
async def view(mission):
    return "Implement!"

@missions_blueprint.route("/add",methods=["GET","POST"])
@require_role(addMissionRole)
async def add():
    return "Implement!"

@missions_blueprint.route("/remove",methods=["GET","POST"])
@require_role(removeMissionRole)
async def remove():
    return "Implement!"

@missions_blueprint.route("/edit",methods=["GET","POST"])
@require_role(editMissionRole)
async def edit():
    return "Implement!"
