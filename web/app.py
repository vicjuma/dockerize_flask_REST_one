"""
Register a new user
Each user will get 10 tokens
Store a sentence on our database for 1 token
If a user stores 1 sentence on our database, he uses 1 token
Retrieve stored sentences using 1 token
Registration uses 0 tokens

"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://db:27017/')
db = client.sentencesDatabase
usersCollection = db.usersCollection


def check_status_code(data_object):
  if "username" not in data_object or "password" not in data_object:
    return 301
  else:
    return 200


class Register(Resource):
  def post(self):
    user = request.get_json()
    status_code = check_status_code(user)
    if status_code != 200:
      message = {
        "message": "Please ensure both the password and username password are provided",
        "status code": status_code
      }
      return message
    username = user['username']
    password = user['password']
    token = 10
    hashedPwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    userData = {
      "username": username,
      "password": hashedPwd.decode('utf-8'),
      "sentence": "",
      "token": token
    }
    usersCollection.insert_one(userData)
    username = usersCollection.find_one()['username']
    return jsonify({
      "message": f"user {username} has been registered successfully",
      "status": 200,
      "password": usersCollection.find_one()['password']
    })
    

class Store(Resource):
  def post(self):
    userData = request.get_json()
    
    username = userData['username']
    password = userData['password']
    sentence = userData['sentence']
    storedInfo = usersCollection.find({"username": username})[0]
    if "username" not in storedInfo:
      return "There is no such user in the database"
    elif storedInfo['username'] == username and bcrypt.checkpw(password.encode('utf8'), storedInfo['password'].encode('utf8')):
        usersCollection.update_one({
          "username": username
        }, {"$set": {"sentence": sentence, "token": int(usersCollection.find_one()['token']) - 1}})
        return jsonify({
      "message": f"user {username} has been updated successfully successfully",
      "status": 200,
      "sentence": usersCollection.find_one()['sentence'],
      "token": usersCollection.find_one()['token']
    })
    else:
      return "passwords did not match"


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

























"""from http import client
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://db:27017/')
db = client.studentDB
studentV = db.studentCollection
studentV.insert_one({"name": "vik"})


def check_status_code(data_object, function_name):
  if function_name == "add":
    if "numberOne" not in data_object or "numberTwo" not in data_object:
      return 301
    else:
      return 200


class Add(Resource):
  def post(self):
    data = request.get_json()
    status_code = check_status_code(data,"add")
    if status_code != 200:
      return jsonify(
        {
          "message": "some data is missing in your message body", "status_code": status_code})
    number_one = int(data['numberOne'])
    number_two = int(data['numberTwo'])
    sum = number_one + number_two
    sumObj = {
      "sum": sum,
      "status_code": status_code
    }
    return jsonify(sumObj)
  
  def get(self):
    student = studentV.find_one({})["name"]
    return f"Hello {student}"


class Sub(Resource):
  def post(self):
    data = request.get_json()
    number_one = int(data['numberOne'])
    number_two = int(data['numberTwo'])
    sub = number_one - number_two
    subObj = {
      "sub": sub
    }
    return jsonify(subObj)
  
  def get(self):
    return "Hello, you want to subtract them up?"


class Mul(Resource):
  def post(self):
    data = request.get_json()
    number_one = int(data['numberOne'])
    number_two = int(data['numberTwo'])
    prod = number_one * number_two
    prodObj = {
      "prod": prod
    }
    return jsonify(prodObj)
  
  def get(self):
    return "Hello, you want to multiply them up?"


class Div(Resource):
  def post(self):
    data = request.get_json()
    number_one = int(data['numberOne'])
    number_two = int(data['numberTwo'])
    div = number_one / number_two
    divObj = {
      "div": div
    }
    return jsonify(divObj)
  
  def get(self):
    return "Hello, you want to divide them up?"


@app.route('/')
def home():
  return "Hello World"

api.add_resource(Add, "/add")
api.add_resource(Sub, "/sub")
api.add_resource(Mul, "/mul")
api.add_resource(Div, "/div")

"""