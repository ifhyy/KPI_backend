import uuid

from project import app
from flask import jsonify, request, g
import datetime

users = {}
categories = {}
records = {}


@app.route("/healthcheck")
def healthcheck():
    response = {
        "current date": datetime.datetime.now().strftime("%d:%m:%Y"),
        "status": "OK"
    }

    return jsonify(response), 200


@app.get("/user")
def get_user():
    user = users[request.args.get("user_id")]
    return user


@app.post("/user")
def create_user():
    user_data = request.get_json()
    username = user_data['username']
    user_id = uuid.uuid4().hex
    user = {"id": user_id, "username": username}
    users[user_id] = user
    return user


@app.delete("/user")
def delete_user():
    user = users.pop(request.args.get("user_id"))
    response = {
        "response": f'{user["username"]} was deleted'
    }
    return jsonify(response)


@app.get("/users")
def get_users():
    return jsonify(users)


@app.get("/category")
def get_category():
    category = categories.get(request.args.get('category_id'))
    return category


@app.post("/category")
def post_category():
    category_data = request.get_json()['category']
    cat_id = uuid.uuid4().hex
    category = {"id": cat_id, "category": category_data}
    categories[cat_id] = category
    return jsonify({cat_id: category})


@app.delete("/category")
def delete_category():
    category = categories.pop(request.args.get('category_id'))
    response = {
        "response": f'category {category} was deleted'
    }
    return jsonify(response)




