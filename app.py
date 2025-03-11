from quart  import Quart
from config import Development,Production

def create_app(mode='Development'):
    app = Quart(__name__)
    app.config.from_object(f"config.{mode}")

    from model import db
    db.init_app(app)

    from index          import index_blueprint
    from crew           import crew_blueprint
    from crewOnboardLog import crewOnboardLog_blueprint
    from missions       import missions_blueprint
    from tasks          import tasks_blueprint
    from duties         import duties_blueprint
    from ranks          import ranks_blueprint

    app.register_blueprint(index_blueprint)
    app.register_blueprint(crew_blueprint)
    app.register_blueprint(crewOnboardLog_blueprint)
    app.register_blueprint(missions_blueprint)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(duties_blueprint)
    app.register_blueprint(ranks_blueprint)

    return app
