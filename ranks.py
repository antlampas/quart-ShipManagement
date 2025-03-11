from quart          import Blueprint,current_app
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,RankTable

ranks_blueprint = Blueprint("ranks",__name__,url_prefix='/ranks',template_folder='templates/default')

class Rank:
    def __init__(self):
        self.Name     = ""
        self.Position = ""

    async def edit(self,Name,Position) -> bool:
        pass

class RankList:
    def __init__(self):
        self.Rank = list()

    async def add(self,rank:Rank) -> bool:
        pass
    async def remove(self,rank:Rank) -> bool:
        pass

@ranks_blueprint.route("/rank/<rank>",methods=["GET"])
async def view():
    return "Implement!"

@ranks_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return "Implement"

@ranks_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return "Implement!"

@ranks_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return "Implement!"
