from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from authorization  import require_role

from model import db
from model import CrewMemberTable
from model import RankTable

from forms import AddRankForm
from forms import RemoveRankForm
from forms import EditRankForm

ranks_blueprint = Blueprint("ranks",__name__,url_prefix='/ranks',template_folder='templates/default')

addRankRole    = ""
removeRankRole = ""
editRankRole   = ""

@ranks_blueprint.route("/",methods=["GET"])
async def view():
    return "Implement!"

@ranks_blueprint.route("/rank/<rank>",methods=["GET"])
async def rank(rank):
    return "Implement!"

@ranks_blueprint.route("/add",methods=["GET","POST"])
@require_role(addRankRole)
async def add():
    form = AddRankForm()
    if request.method == 'GET':
        return await render_template("ranksAdd.html",FORM=form,SECTIONNAME="Rank")
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
                return await render_template("ranksAdd.html",FORM=form,SECTIONNAME="Ranks",MESSAGE=str(e))
            return await render_template("ranksAdd.html",FORM=form,SECTIONNAME="Ranks",MESSAGE="Success")
    else:
        return await render_template("error.html",error="Invalid method",SECTIONNAME="Ranks")

@ranks_blueprint.route("/remove",methods=["GET","POST"])
@require_role(removeRankRole)
async def remove():
    return "Implement!"

@ranks_blueprint.route("/edit",methods=["GET","POST"])
@require_role(editRankRole)
async def edit():
    return "Implement!"
