from flask import request, jsonify
from markupsafe import escape
from utils.json_encode import json_encode
from bson.objectid import ObjectId


class UserController:
  @staticmethod
  def get_users(db):
    users = db.users.find()
    response = []
    
    return jsonify([json_encode(user) for user in users])

  @staticmethod
  def get_one_user(db, id):
    try:
      user = db.users.find_one({'_id': ObjectId(id)})
      return jsonify(json_encode(user))
    except:
      return {'message': 'An error occured'}, 500
    

  @staticmethod
  def insert_user(db):
    created_user = db.users.insert_one({
      'username': request.form['username']
    })
    user = db.users.find_one({'_id': created_user.inserted_id})

    return jsonify(json_encode(user))

  @staticmethod
  def update_user(db, id):
    updated_user = db.users.update_one({'_id': ObjectId(id)}, {
      '$set': {
        'username': request.form['username']
      }
    })
    user = db.users.find_one({'_id': ObjectId(id)})

    return jsonify(json_encode(user))

  @staticmethod
  def delete_user(db, id):
    updated_user = db.users.delete_one({'_id': ObjectId(id)})

    return {
      'message': 'Deleted successfully'
    }