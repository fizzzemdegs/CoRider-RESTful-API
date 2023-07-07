from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))


app = Flask(__name__)
uri = "mongodb+srv://<userid>:<password>@corider.ayks3du.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.corider.user_info



@app.route('/')
def landing_page():
    data = [
        "Corider Task",
        {
            "/users [GET]": "get all user",
            "/users/<id> [GET]": "get user by id",
            "/users [POST]": "create new user",
            "/users/<id> [POST]": "update user",
            "/users/<id> [DELETE]": "delete user"
        }
    ]
    return jsonify(data)


@app.route('/users', methods=['GET'])
def get_user():
    try:
        json_result = parse_json(collection.find())
        return json_result
    except PyMongoError as e:
        return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


@app.route('/users/<int:id>', methods=['GET'])
def get_user_id(id):
    try:
        json_result = parse_json(collection.find({"_id": id}))
        return json_result
    except PyMongoError as e:
        return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


@app.route('/users', methods=['POST'])
def crete_user():  # put application's code here
    try:
        data = request.get_json()
        result = collection.insert_one(data[0])
        return jsonify('Document created', {"id": result.inserted_id})
    except PyMongoError as e:
        return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


@app.route('/users/<int:id>', methods=['PUT'])
def update_user_id(id):  # put application's code here
    try:
        data = request.get_json()
        filter = {'_id': id}
        update = {'$set': data[0]}
        result = collection.update_one(filter, update)
        return jsonify("Document updated:")

    except PyMongoError as e:
        return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user_id(id):  # put application's code here
    try:
        result = collection.delete_many({"_id": id})
        return jsonify('Document deleted:', result.deleted_count)
    except PyMongoError as e:
        return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)