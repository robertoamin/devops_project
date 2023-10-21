from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from flask import request, send_file
from marshmallow import ValidationError
# from blacklist.config import BaseConfig
import os
from blacklist.api.schemas.users import LoginSchema, UserSchema
from blacklist.extensions import db
from blacklist.models import User

login_schema = LoginSchema()
user_schema =  UserSchema()


class LoginView(Resource):
    @staticmethod
    def post():
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            data = login_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        user = User.query.filter(User.email == data.get('email')).first()

        if user is None:
            return {"message": "Email or password incorrect"}, 401

        token = create_access_token(identity=user.id)

        return {
                   "message": "Success",
                   "token": token,
                   "id": user.id
               }, 200


class SignUpView(Resource):
    @staticmethod
    def post():
        json_data = request.get_json()
        # If using the base configuration
        # config = BaseConfig()
        # print(config.SQLALCHEMY_DATABASE_URI)
        print(os.getenv('POSTGRES_USER'))
        print(os.getenv('POSTGRES_HOST'))
        print(os.getenv('APP_SETTINGS'))
        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        user = User.query.filter(User.email == data.email).first()

        if user is not None:
            return {"message": "User already exists"}, 409

        user = User(
            password=data.password,
            email=data.email
        )
        db.session.add(user)
        db.session.commit()

        return {"status": "OK"}


def initialize_routes(api):
    api.add_resource(LoginView, '/login')
    api.add_resource(SignUpView, '/sign-up')