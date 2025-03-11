from quart          import Blueprint,current_app
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,DutyTable

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

@duties_blueprint.route("/duty/<duty>",methods=["GET"])
async def view():
    return "Implement!"

@duties_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return "Implement"

@duties_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return "Implement!"

@duties_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return "Implement!"
