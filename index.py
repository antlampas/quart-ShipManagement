from quart import Blueprint,current_app,render_template,request

index_blueprint = Blueprint("index",__name__,template_folder='templates/default')

@index_blueprint.route("/")
async def index():
    return await render_template("index.html",SECTIONNAME='Home Page')
