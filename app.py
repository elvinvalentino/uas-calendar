from flask import Flask, request
from flask_pymongo import PyMongo
from controllers.UserController import UserController
from controllers.EventController import EventController
from controllers.CategoryController import CategoryController
from dotenv import load_dotenv, dotenv_values

# load_dotenv()
config = dotenv_values('.env')

app = Flask(__name__)
app.config["MONGO_URI"] = config['MONGO_URIS']
mongo = PyMongo(app)
db = mongo.db

########################################################################
# user
########################################################################
@app.route("/api/users", methods=['GET', 'POST'])
def user():
  if request.method == 'GET':
    return UserController.get_users(db)
  elif request.method == 'POST':
    return UserController.insert_user(db)

# @app.route('/api/users/<id>', methods=['GET', 'PUT', 'DELETE'])
# def one_user(id):
#   if request.method == 'GET':
#     return UserController.get_one_user(db, id)
#   elif request.method == 'PUT':
#     return UserController.update_user(db, id)
#   elif request.method == 'DELETE':
#     return UserController.delete_user(db, id)

################################################################################
# events
################################################################################
@app.route("/api/events", methods=['GET', 'POST'])
def event():
  if request.method == 'GET':
    return EventController.get_events(db)
  elif request.method == 'POST':
    return EventController.insert_event(db)

@app.route('/api/events/<id>', methods=['GET', 'PUT', 'DELETE'])
def one_event(id):
  if request.method == 'GET':
    return EventController.get_one_event(db, id)
  elif request.method == 'PUT':
    return EventController.update_event(db, id)
  elif request.method == 'DELETE':
    return EventController.delete_event(db, id)

################################################################################
# category
################################################################################
@app.route("/api/categories", methods=['GET', 'POST'])
def category():
  if request.method == 'GET':
    return CategoryController.get_categories(db)
  elif request.method == 'POST':
    return CategoryController.insert_category(db)

@app.route('/api/categories/<id>', methods=['GET', 'PUT', 'DELETE'])
def one_category(id):
  if request.method == 'GET':
    return CategoryController.get_one_category(db, id)
  elif request.method == 'PUT':
    return CategoryController.update_category(db, id)
  elif request.method == 'DELETE':
    return CategoryController.delete_category(db, id)