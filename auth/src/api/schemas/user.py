import marshmallow as ma


class UserLoginSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)


class UserRegisterSchema(ma.Schema):
    username = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    password = ma.fields.String(required=True)


class UserInfoSchema(ma.Schema):
    class Meta:
        include = {
            'User-Agent': ma.fields.String(),
            'X-Forwarded-For': ma.fields.String(),
        }
        ordered = True


class UserChangeUsernameSchema(ma.Schema):
    password = ma.fields.String(required=True)
    username_new = ma.fields.String(required=True)


class UserChangePasswordSchema(ma.Schema):
    password_new = ma.fields.String(required=True)
    password_old = ma.fields.String(required=True)


class UserAssignRoleSchema(ma.Schema):
    role_id = ma.fields.UUID(required=True)
