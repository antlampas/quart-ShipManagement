from quart import current_app,Blueprint

from model import db,CrewMemberTable,TaskTable,MemberTaskLogEntryTable

tasks_blueprint = Blueprint("tasks",__name__,url_prefix='/tasks',template_folder='templates/default')

class Task:
    async def __init__():
        self.Name             = ""
        self.Description      = ""
        self.Objective        = ""
        self.RequiredDuration = ""
        self.StartedAt        = ""
        self.EndedAt          = ""
        self.Status           = ""

    async def edit(self,name,description,objective,requiredDuration,startedAt,endedAt,status) -> bool:
        pass

class TaskList:
    async def __init__():
        self.Task = list()

    async def add(task:Task) -> bool:
        pass
    async def remove(task:Task) -> bool:
        pass

@tasks_blueprint.route("/task/<task>")
async def view(task):
    return "Implement!"

@tasks_blueprint.route("/add")
async def add():
    return "Implement!"

@tasks_blueprint.route("/remove")
async def remove():
    return "Implement!"

@tasks_blueprint.route("/edit")
async def edit():
    return "Implement!"
