import marshmallow as ma


class RoleSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()


class RoleSchemaModify(ma.Schema):
    name = ma.fields.String()
    description = ma.fields.String()

    @ma.validates_schema
    def validate_at_least_one_is_required(self, data, **kwargs) -> None:
        if not data.get('name') and not data.get('description'):
            raise ma.ValidationError('At least one of the fields is required')


class RoleSchemaCreate(ma.Schema):
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
