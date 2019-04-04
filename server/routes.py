from server import app, api
from flask import request
from flask_restful import Resource
import requests
import server.back_end_processor as be


class GetQuote(Resource):

    def post(self):
        user_input = request.get_json()
        response = be.quote(user_input["user_input"])
        return response


api.add_resource(GetQuote, "/getquote/")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
