from client import app, api
from flask import render_template, request, jsonify
from flask_restful import Resource
import requests
import json
from time import sleep


def send_recieve(to_send):
    post_request = requests.post(
        "http://127.0.0.1:5001/getquote/", json=to_send
    )

    return post_request.text


# Routes


@app.route("/", methods=["POST", "GET"])
def index():

    response = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        user_input = {"user_input": user_input}
        response = send_recieve(user_input)

    return render_template("index.html", output=response)
