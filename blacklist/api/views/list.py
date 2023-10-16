from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from marshmallow import ValidationError

from ...models import BlackList
from flask import Flask, request
from blacklist.extensions import db
from blacklist.api.schemas.blacklist import BlacklistSchema
import uuid

blacklist_schema = BlacklistSchema()

class BlackListView(Resource):
    @jwt_required()
    def get(self, email):
        entry = BlackList.query.filter_by(email=email).first()
        if entry:
            return {"blacklisted": True, "reason": entry.blocked_reason}, 200
        else:
            return {"blacklisted": False, "reason": None}, 200

    @jwt_required()
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            data = blacklist_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        email = data.email
        blocked_reason = data.blocked_reason

        # Capturar la dirección IP
        ip_address = request.remote_addr

        # Crear entrada en la lista negra
        blacklist_entry = BlackList(email=email, blocked_reason=blocked_reason, ip_address=ip_address)
        db.session.add(blacklist_entry)
        db.session.commit()

        return {"message": "Email añadido a la lista negra con éxito"}, 201

def initialize_routes(api):
    api.add_resource(BlackListView, '/blacklists', '/blacklists/<string:email>')