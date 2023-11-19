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
            return user, 200
        return jsonify({"message": f"user {user_id} does not exist"}), 404
    return jsonify({"message": "Required argument \'used_id\' wasn't passed"}), 400


@app.post("/user")
def create_user():
    username = request.get_json().get("username", None)
    if username:
        user_id = uuid.uuid4().hex
        user = {"id": user_id, "username": username}
        users[user_id] = user
        return user, 201
    return jsonify({"message": "Required data \'username\' wasn't passed"}), 400


@app.delete("/user")
def delete_user():
    user_id = request.args.get("user_id", None)
    if user_id:
        try:
            user = users.pop(user_id)
            return jsonify({"message": f'{user["username"]} was deleted'}), 200
        except KeyError as e:
            return jsonify({"message": f"user {user_id} does not exist"}), 404
    return jsonify({"message": "required argument \'used_id\' wasn't passed"}), 400


@app.get("/users")
def get_users():
    return jsonify(users), 200


@app.get("/category")
def get_category():
    category_id = request.args.get('category_id', None)
    if category_id:
        category = categories.get(category_id, None)
        if category:
            return category, 200
        return jsonify({"message": f"category {category_id} does not exist"}), 404
    return jsonify({"message": "Required argument \'category_id\' wasn't passed"}), 400


@app.post("/category")
def create_category():
    category_name = request.get_json().get("category", None)
    if category_name:
        cat_id = uuid.uuid4().hex
        category = {"id": cat_id, "category": category_name}
        categories[cat_id] = category
        return category, 201
    return jsonify({"message": "Required data \'category\' wasn't passed"}), 400


@app.delete("/category")
def delete_category():
    category_id = request.args.get("category_id", None)
    if category_id:
        try:
            category = categories.pop(category_id)
            return jsonify({"message": f'{category["category"]} was deleted'}), 200
        except KeyError as e:
            return jsonify({"message": f"category {category_id} does not exist"}), 404
    return jsonify({"message": "required argument \'category_id\' wasn't passed"}), 400


@app.post("/record")
def create_record():
    record_user_id = request.get_json().get("user_id", None)
    if not record_user_id:
        return jsonify({"message": "required data \'user_id\' wasn't passed"}), 400
    record_category_id = request.get_json().get("category_id", None)
    if not record_category_id:
        return jsonify({"message": "required data \'category_id\' wasn't passed"}), 400
    date_and_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    expenses = random.randint(1, 100)
    record_id = uuid.uuid4().hex
    record = {"id": record_id, "user_id": record_user_id, "category_id": record_category_id,
              "date_and_time": date_and_time, "expenses": expenses}
    records[record_id] = record
    return record, 201


@app.delete("/record")
def delete_record():
    record_id = request.args.get("record_id", None)
    if record_id:
        try:
            record = records.pop(record_id)
            return jsonify({"message": f'record {record_id} was deleted'}), 200
        except KeyError as e:
            return jsonify({"message": f"record {record_id} does not exist"}), 404
    return jsonify({"message": "required argument \'record_id\' wasn't passed"}), 400


@app.get("/record")
def get_record():
    record_id = request.args.get("record_id")
    category_id = request.args.get("category_id")
    user_id = request.args.get("user_id")

    if record_id:
        record = records.get(record_id)
        if record:
            return jsonify(record), 200
        return jsonify({"message": f"Record {record_id} does not exist"}), 404

    results = {}
    for key, value in records.items():
        if user_id and category_id:
            if value['user_id'] == user_id and value['category_id'] == category_id:
                results[key] = value
        elif category_id:
            if value['category_id'] == category_id:
                results[key] = value
        elif user_id:
            if value['user_id'] == user_id:
                results[key] = value

    if results:
        return jsonify(results), 200
    return jsonify({"message": "No records found"}), 404
