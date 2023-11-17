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
        user = users.get(user_id, None)
        if user:
            return users[user_id], 200
        return jsonify({"response": f"user {user_id} does not exist"}), 404
    return jsonify({"response": "Required argument \'used_id\' wasn't passed"}), 400


@app.post("/user")
def create_user():
    username = request.get_json().get("username", None)
    if username:
        user_id = uuid.uuid4().hex
        user = {"id": user_id, "username": username}
        users[user_id] = user
        return user, 201
    return jsonify({"response": "Required data \'username\' wasn't passed"}), 400


@app.delete("/user")
def delete_user():
    user_id = request.args.get("user_id", None)
    if user_id:
        try:
            user = users.pop(user_id)
            return jsonify({"response": f'{user["username"]} was deleted'}), 200
        except KeyError as e:
            return jsonify({"response": f"user {user_id} does not exist"}), 404
    return jsonify({"response": "required argument \'used_id\' wasn't passed"}), 400


@app.get("/users")
def get_users():
    return jsonify({users.values()}), 200


@app.get("/category")
def get_category():
    category_id = request.args.get('category_id', None)
    if category_id:
        category = categories.get(category_id, None)
        if category:
            return categories[category_id], 200
        return jsonify({"response": f"category {category_id} does not exist"}), 404
    return jsonify({"response": "Required argument \'category_id\' wasn't passed"}), 400


@app.post("/category")
def create_category():
    category_name = request.get_json().get("category", None)
    if category_name:
        cat_id = uuid.uuid4().hex
        category = {"id": cat_id, "category": category_name}
        categories[cat_id] = category
        return category, 201
    return jsonify({"response": "Required data \'category\' wasn't passed"}), 400


@app.delete("/category")
def delete_category():
    category_id = request.args.get("category_id", None)
    if category_id:
        try:
            category = categories.pop(category_id)
            return jsonify({"response": f'{category["category"]} was deleted'}), 200
        except KeyError as e:
            return jsonify({"response": f"category {category_id} does not exist"}), 404
    return jsonify({"response": "required argument \'category_id\' wasn't passed"}), 400


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


# @app.delete
# def delete_record():
#     pass
#     # record_id = request.args.get("request", None)
#     # if record_id
#
