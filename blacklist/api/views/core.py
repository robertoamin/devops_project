from flask_restful import Api, Resource


class HealthView(Resource):
    @staticmethod
    def get():
        return {"status": "OK"}


def initialize_routes(api):
    api.add_resource(HealthView, '/health')