from blacklist.extensions import db, pwd_context
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid

class BlackList(db.Model):
    """Blacklist model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)