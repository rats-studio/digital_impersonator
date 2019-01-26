from communicator import Communicator
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    """ main view

    Takes input-string and passes it through the communicator class
    """

    # set output to none
    output = None

    print("maggormaggormaggor")

    # check for http-request
    if request.method == "POST":

        # fetch data in request
        entry = request.form["aar_input"]
        print("!!!" + entry)

        # put data into python-dict to use as json
        entry = {"entry_string": entry}

        # send through Communicator  and store response in 'output'
        output = Communicator.send_recieve(entry)

    # render webapp
    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run(port=5003)
