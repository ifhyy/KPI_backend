from project import app
from flask import jsonify
import datetime


@app.route("/healthcheck")
def healthcheck():
    response = {
        "current date": datetime.datetime.now().strftime("%d:%m:%Y"),
        "status": "OK"
    }

    return jsonify(response), 200

