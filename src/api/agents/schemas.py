from marshmallow import Schema, fields as f, validate


class AgentSkillSchema(Schema):
    name = f.String()
    type = f.String(validate=validate.OneOf(["Python"]))
    path = f.String()


class AgentSchema(Schema):
    name = f.String()
    skills = f.List(f.Nested(AgentSkillSchema))


class AgentQuerySchema(Schema):
    query = f.String()


class AgentQueryResponseSchema(Schema):
    response = f.String()
