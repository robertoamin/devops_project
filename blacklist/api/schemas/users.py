from flask_marshmallow.fields import fields
from marshmallow import validates_schema, ValidationError

from blacklist.extensions import ma, db
from blacklist.models import User


class LoginSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)

    password = fields.String(required=True, load_only=True)
    password2 = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                raise ValidationError('Passwords must match', 'password2')
        else:
            raise ValidationError('Password 2 are required')