from quart import Blueprint
from quart import current_app
from quart import render_template
from quart import request
from quart import session

index_blueprint = Blueprint("index",__name__,template_folder='templates/default')

@index_blueprint.route("/")
async def index():
    return await render_template("index.html",SECTIONNAME='Home Page')
