from sqlalchemy.ext.hybrid import hybrid_property

from blacklist.extensions import db, pwd_context


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def verify(self, value):
        return pwd_context.verify(value, self._password)

    def __repr__(self):
        return "<User %s>" % self.email

