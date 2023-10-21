from marshmallow import validates_schema, ValidationError
from blacklist.extensions import ma, db
from blacklist.models import BlackList
import re

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlackList
        sqla_session = db.session
        load_instance = True
        exclude = ("ip_address",)

    @validates_schema
    def validate_data(self, data, **kwargs):
        if 'email' in data and 'blocked_reason' in data:
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, data['email']):
                raise ValidationError('Invalid email format', 'email')
        else:
            raise ValidationError('Missing fields')