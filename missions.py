from quart import current_app,Blueprint

from model import db,CrewMemberTable,TaskTable,MissionTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable

missions_blueprint = Blueprint("missions",__name__,url_prefix='/missions',template_folder='templates')

class Mission:
    def __init__(self):
        self.Name             = ""
        self.Description      = ""
        self.RequiredDuration = ""
        self.StartedAt        = ""
        self.EndedAt          = ""
        self.Tasks            = list()
        self.Status           = ""

    async def edit(self,mission):
        pass

class MissionList:
    def __init__(self):
        self.Mission = list()

    async def add(mission:Mission):
        pass
    async def remove(mission:Mission):
        pass

@missions_blueprint.route("/mission/<mission>",methods=["GET"])
async def view(mission):
    return "Implement!"

@missions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return "Implement!"

@missions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return "Implement!"

@missions_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return "Implement!"
