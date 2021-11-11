from flask import request, jsonify
from markupsafe import escape
from utils.json_encode import json_encode
from bson.objectid import ObjectId
from utils.get_random import get_random_string


class UserController:
  @staticmethod
  def get_users(db):
    try:
      users = db.users.find()
      response = []
      return jsonify([json_encode(user) for user in users])
    except:
      return {'message': 'An error occurred'}, 500

  

  @staticmethod
  def get_one_user(db, id):
    try:
      user = db.users.find_one({'_id': ObjectId(id)})
      return jsonify(json_encode(user))
    except:
      return {'message': 'An error occurred'}, 500
    

  @staticmethod
  def insert_user(db):
    try:
      ##token
      at = get_random_string(32)

      created_user = db.users.insert_one({
        'email': request.form['email'],
        'username': request.form['username'],
        'profilePicture': request.form['profilePicture'],
        'accessToken': at
      })
      user = db.users.find_one({'_id': created_user.inserted_id})

      ##preset
      db.categories.insert_one({
        'userId': created_user.inserted_id,
        'name': 'appointment',
        'hex': '#EB4A2F',
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
          'email': request.form['email'],
          'username': request.form['username'],
          'profilePicture': request.form['profilePicture']
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