from quart import current_app,Blueprint

from authorization  import require_role

from model import db
from model import CrewMemberTable
from model import TaskTable
from model import MemberTaskLogEntryTable

tasks_blueprint = Blueprint("tasks",__name__,url_prefix='/tasks',template_folder='templates/default')

sectionName = "Tasks"

addTaskRole    = ""
removeTaskRole = ""
editTaskRole   = ""

@tasks_blueprint.route("/task/<task>")
async def view(task):
    return "Implement!"

@tasks_blueprint.route("/add")
@require_role(addTaskRole)
async def add():
    return "Implement!"

@tasks_blueprint.route("/remove")
@require_role(removeTaskRole)
async def remove():
    return "Implement!"

@tasks_blueprint.route("/edit")
@require_role(editTaskRole)
async def edit():
    return "Implement!"
