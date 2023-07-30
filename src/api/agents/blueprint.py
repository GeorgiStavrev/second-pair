import flask
from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView

from api.agents.schemas import AgentSchema, AgentQuerySchema, AgentQueryResponseSchema

from services import storage

blp = Blueprint(
    "agents",
    "agents",
    url_prefix="/api/v1/agents",
    description="Agents API.",
)


@blp.route("/")
class CreateAgent(MethodView):
    @blp.arguments(AgentSchema, location="json")
    @blp.response(200)
    def post(self, args):
        storage.write_agent(**args)
        return flask.Response(status=201)


@blp.route("/")
class GetAllAgents(MethodView):
    @blp.response(200, AgentSchema)
    def get(self, agent_id):
        agents = storage.read_agents()
        return jsonify([a.get("name") for a in agents])


@blp.route("/<name>")
class GetAgent(MethodView):
    @blp.response(200, AgentSchema)
    def get(self, name: str):
        agent = storage.read_agent(name)
        return jsonify(agent)


@blp.route("/<name>/query")
class QueryAgent(MethodView):
    @blp.arguments(AgentQuerySchema, location="json")
    @blp.response(200, AgentQueryResponseSchema)
    def post(self, *args: str, **kwargs: dict):
        agent_response = "Empty"
        response = {
            "response": agent_response
        }
        return jsonify(response)
