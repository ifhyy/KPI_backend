import random
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
    user_id = request.args.get("user_id", None)
    if user_id:
        return users[user_id]
    return jsonify({"response": f"user {user_id} does not exist"})


@app.post("/user")
def create_user():
    username = request.get_json()['username']
    user_id = uuid.uuid4().hex
    user = {"id": user_id, "username": username}
    users[user_id] = user
    return user


@app.delete("/user")
def delete_user():
    user_id = request.args.get("user_id", None)
    if user_id:
        user = users.pop(user_id)
        response = {
            "response": f'{user["username"]} was deleted'
        }
        return jsonify(response)
    return jsonify({"response": f"user {user_id} does not exist"})


@app.get("/users")
def get_users():
    return jsonify(users)


@app.get("/category")
def get_category():
    category_id = request.args.get('category_id', None)
    if category_id:
        return categories[category_id]
    return jsonify({"response": f"category {category_id} does not exist"})


@app.post("/category")
def post_category():
    category_name = request.get_json()['category']
    cat_id = uuid.uuid4().hex
    category = {"id": cat_id, "category": category_name}
    categories[cat_id] = category
    return jsonify({cat_id: category})


@app.delete("/category")
def delete_category():
    category_id = request.args.get("category_id", None)
    if category_id:
        category = categories.pop(category_id)
        response = {
            "response": f'{category["category"]} was deleted'
        }
        return jsonify(response)
    return jsonify({"response": f"category {category_id} does not exist"})


@app.post("/record")
def create_record():
    record_user_id = request.args.get("user_id", None)
    record_category_id = request.args.get("category_id", None)
    date_and_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    expenses = random.randint(1, 100)
    record_id = uuid.uuid4().hex
    record = {"id": record_id, "user_id": record_user_id, "category_id": record_category_id,
              "date_and_time": date_and_time, "expenses": expenses}
    records[record_id] = record
    return record

