from flask import Flask
from flask_restful import Api
# from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')

api = Api(app)

from client import routes
