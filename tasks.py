from quart import current_app,Blueprint

from authorization  import require_role

from model import db
from model import CrewMemberTable
from model import TaskTable
from model import MemberTaskLogEntryTable

from authorization  import require_role
from authorization  import require_login
from permissions    import TasksPermissions

tasks_blueprint = Blueprint("tasks",__name__,url_prefix='/tasks',template_folder='templates/default')

sectionName = "Tasks"

@tasks_blueprint.route("/task/<task>")
@require_login
async def view(task):
    return "Implement!"

@tasks_blueprint.route("/add")
@require_role(TasksPermissions.addTaskRole)
async def add():
    return "Implement!"

@tasks_blueprint.route("/remove")
@require_role(TasksPermissions.removeTaskRole)
async def remove():
    return "Implement!"

@tasks_blueprint.route("/edit")
@require_role(TasksPermissions.editTaskRole)
async def edit():
    return "Implement!"
