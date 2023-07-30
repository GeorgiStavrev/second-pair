from marshmallow import Schema, fields as f


class AgentSchema(Schema):
    name = f.String()
    skills = f.List(f.String)


class AgentQuerySchema(Schema):
    query = f.String()


class AgentQueryResponseSchema(Schema):
    response = f.String()
