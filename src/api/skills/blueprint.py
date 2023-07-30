import flask
from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView

from api.skills.schemas import PythonSkill
from services import storage

blp = Blueprint(
    "skills",
    "skills",
    url_prefix="/api/v1/skills",
    description="Skills API. Allows to define skills for agents to use.",
)


@blp.route("/")
class GetAllSkills(MethodView):
    @blp.response(200)
    def get(self):
        skills = storage.read_skills()
        return jsonify([s.get("name") for s in skills])


@blp.route("/python")
class AddPythonSkill(MethodView):
    @blp.arguments(PythonSkill, location="json")
    @blp.response(200)
    def post(self, args):
        name = args.get("name")
        description = args.get("description")
        code = args.get("code")
        storage.write_skill(name, description, code)
        return flask.Response(status=201)
