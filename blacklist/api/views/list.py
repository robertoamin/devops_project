from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Api, Resource



class BlackListView(Resource):
    @jwt_required()
    def get(self, email):
        return [], 200

    @jwt_required()
    def post(self):
        return {"status": "OK"}, 201



def initialize_routes(api):
    api.add_resource(BlackListView, '/blacklists', '/blacklists/<string:email>')