from marshmallow import Schema, fields as f


class PythonSkill(Schema):
    name = f.String(max=50)
    description = f.String(max=250)
    code = f.String()
