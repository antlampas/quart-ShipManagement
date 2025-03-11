from quart          import Blueprint,current_app,request,render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,RankTable
from forms import AddRankForm,RemoveRankForm,EditRankForm

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

@ranks_blueprint.route("/",methods=["GET"])
async def view():
    return "Implement!"

@ranks_blueprint.route("/rank/<rank>",methods=["GET"])
async def rank(rank):
    return "Implement!"

@ranks_blueprint.route("/add",methods=["GET","POST"])
async def add():
    form = AddRankForm()
    if request.method == 'GET':
        return await render_template("rankAdd.html",FORM=form,SECTIONNAME="Rank")
    elif request.method == 'POST':
        name         = (await request.form)['Name']
        description  = (await request.form)['Description']
        rank         = RankTable(Name=name,Description=description)
        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(rank)
                        s.commit()
            except Exception as e:
                return await render_template("rankAdd.html",FORM=form,SECTIONNAME="Ranks",MESSAGE=str(e))
            return await render_template("rankAdd.html",FORM=form,SECTIONNAME="Ranks",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Ranks")

@ranks_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return "Implement!"

@ranks_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return "Implement!"
