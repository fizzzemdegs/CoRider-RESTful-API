from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))


app = Flask(__name__)
api = Api(app)

uri = "mongodb+srv://<username>:<password>@corider.ayks3du.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.corider.user_info


class landing(Resource):
    def get(self):
        data = {
            "CoRider Task":
            {
                "/users [GET]": "get all user",
                "/users/<id> [GET]": "get user by id",
                "/users [POST]": "create new user",
                "/users/<id> [PUT]": "update user",
                "/users/<id> [DELETE]": "delete user"
            }
        }
        return jsonify(data)
class users(Resource):

    def get(self):
        try:
            json_result = parse_json(collection.find())
            return json_result
        except PyMongoError as e:
            return jsonify('Error!', {'MongoDB Error Code': str(e.code)})

    def post(self):
        try:
            data = request.get_json()
            print(data)
            result = collection.insert_one(data[0])
            return jsonify('Document created', {"id": result.inserted_id})
        except PyMongoError as e:
            return jsonify('Error!', {'MongoDB Error Code': str(e.code)})




class usersId(Resource):

    def get(self, user_id):
        try:
            json_result = parse_json(collection.find({"_id": user_id}))
            return json_result
        except PyMongoError as e:
            return jsonify('Error!', {'MongoDB Error Code': str(e.code)})

    def put(self, user_id):
        try:
            data = request.get_json()
            filter = {'_id': user_id}
            update = {'$set': data[0]}
            result = collection.update_one(filter, update)
            return jsonify("Document updated!")

        except PyMongoError as e:
            return jsonify('Error!', {'MongoDB Error Code': str(e.code)})

    def delete(self, user_id):
        try:
            result = collection.delete_many({"_id": user_id})
            return jsonify({'Document deleted': result.deleted_count})
        except PyMongoError as e:
            return jsonify('Error!', {'MongoDB Error Code': str(e.code)})


api.add_resource(landing, "/")
api.add_resource(users, "/users")
api.add_resource(usersId, "/users/<int:user_id>")

if __name__ == '__main__':
    app.run()
