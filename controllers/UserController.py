from flask import request, jsonify
from expetions.token import InvlidToken, NoToken
from utils.get_current_user import get_current_user
from utils.json_encode import json_encode
from bson.objectid import ObjectId
from utils.get_random import get_random_string


class UserController:
  @staticmethod
  def me(db):
    try:
      user = get_current_user(db)
      return jsonify(json_encode(user))
    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except:
      return {'message': 'An error occurred'}, 500

  @staticmethod
  def get_users(db):
    try:
      users = db.users.find()
      return jsonify([json_encode(user, [], ['accessToken']) for user in users])
    except:
      return {'message': 'An error occurred'}, 500

  

  @staticmethod
  def get_one_user(db, id):
    try:
      user = db.users.find_one({'_id': ObjectId(id)})
      return jsonify(json_encode(user, [], 'accessToken'))
    except:
      return {'message': 'An error occurred'}, 500
    

  @staticmethod
  def insert_user(db):
    try:
      ## check if user is already exists or not
      ## if exists returning the existing user
      isExists = db.users.find_one({'email': request.json['email']})
      if isExists is not None:
        return jsonify(json_encode(isExists))

      ##token
      at = get_random_string(32)

      created_user = db.users.insert_one({
        'email': request.json['email'],
        'username': request.json['username'],
        'profilePicture': request.json['profilePicture'],
        'accessToken': at
      })
      user = db.users.find_one({'_id': created_user.inserted_id})

      ##preset
      db.categories.insert_one({
        'userId': created_user.inserted_id,
        'name': 'Appointment / task',
        'hex': '#ccc',
        'isPreset': True
      })

      return jsonify(json_encode(user))

    except:
      return {'message': 'An error occurred'}, 500

  @staticmethod
  def update_user(db, id):
    try:
      updated_user = db.users.update_one({'_id': ObjectId(id)}, {
        '$set': {
          'email': request.json['email'],
          'username': request.json['username'],
          'profilePicture': request.json['profilePicture']
        }
      })
      user = db.users.find_one({'_id': ObjectId(id)})

      return jsonify(json_encode(user))
    
    except:
      return {'message': 'An error occurred'}, 500

  @staticmethod
  def delete_user(db, id):
    try:
      updated_user = db.users.delete_one({'_id': ObjectId(id)})

      return {
        'message': 'Deleted successfully'
      }
    except:
      return {'message': 'An error occurred'}, 500