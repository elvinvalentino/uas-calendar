from flask import Flask, request
from flask_pymongo import PyMongo
from controllers.UserController import UserController
from dotenv import load_dotenv, dotenv_values

# load_dotenv()
config = dotenv_values('.env')

app = Flask(__name__)
app.config["MONGO_URI"] = config['MONGO_URI']
mongo = PyMongo(app)
db = mongo.db

@app.route("/api/users", methods=['GET', 'POST'])
def user():
  if request.method == 'GET':
    return UserController.get_users(db)
  elif request.method == 'POST':
    return UserController.insert_user(db)

@app.route('/api/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(id):
  if request.method == 'GET':
    return UserController.get_one_user(db, id)
  elif request.method == 'PUT':
    return UserController.update_user(db, id)
  elif request.method == 'DELETE':
    return UserController.delete_user(db, id)
