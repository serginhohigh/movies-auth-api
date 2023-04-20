import marshmallow as ma


class DeviceSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    user_agent = ma.fields.String()
    ip_address = ma.fields.String()
    date_auth = ma.fields.DateTime()
    date_logout = ma.fields.DateTime()
