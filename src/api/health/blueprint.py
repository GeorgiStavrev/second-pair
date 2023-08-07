import flask
from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint(
    "health",
    "health",
    url_prefix="/api/v1/health",
    description="squad-service service health.",
)


@blp.route("/")
class Health(MethodView):
    @blp.response(200)
    def get(self):
        return flask.Response(
            status=200, response="Service squad-service is healthy!", mimetype="text/plain"
        )
