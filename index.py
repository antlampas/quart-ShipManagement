from quart import Blueprint
from quart import current_app
from quart import render_template
from quart import request
from quart import session

from jose import jwt

from standardReturn import standardReturn

index_blueprint = Blueprint("index",__name__,template_folder='templates/default')

sectionName = "Home Page"

@index_blueprint.route("/")
async def index():
    return await standardReturn("index.html",sectionName)
