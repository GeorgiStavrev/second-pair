import os
import flask
from flask.json import JSONEncoder
from datetime import date, datetime
from flask_smorest import Api
from flask_cors import CORS

from config import APP_SECRET
from api.health.blueprint import blp as health_blueprint
from api.skills.blueprint import blp as skills_blueprint
from api.agents.blueprint import blp as agents_blueprint


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = flask.Flask(__name__)
app.secret_key = APP_SECRET
app.config.from_object("config.Config")
CORS(app, supports_credentials=True)

# Register API
api = Api(app)
api.register_blueprint(health_blueprint)
api.register_blueprint(skills_blueprint)
api.register_blueprint(agents_blueprint)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder
