from communicator import Communicator
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=["POST", "GET"])
def index():
    """ main view

    Takes input-string and passes it through the communicator class
    """

    # set response to none
    response = None

    # check for http-request
    if request.method == "POST":

        # fetch data in request
        user_input = request.form["submit"]

        # put data into python-dict to use as json
        user_input = {"submit": user_input}

        # send through Communicator and store response in 'output'
        response = Communicator.send_recieve(user_input)

    # render webapp
    return render_template("index.html", output=response)


if __name__ == "__main__":
    app.run(port=5003)
