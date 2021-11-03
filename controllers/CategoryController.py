from flask import request, jsonify
from markupsafe import escape
from utils.json_encode import json_encode
from bson.objectid import ObjectId


class CategoryController:
  @staticmethod
  def get_categories(db):
    try:
      categories = db.categories.find()
      response = []
    
      return jsonify([json_encode(category) for category in categories])

    except:
      return {'message': 'An error occured'}, 500

  @staticmethod
  def get_one_category(db, id):
    try:
      category = db.categories.find_one({'_id': ObjectId(id)})
      return jsonify(json_encode(category))
    except:
      return {'message': 'An error occured'}, 500
    

  @staticmethod
  def insert_category(db):
    try:
      created_category = db.categories.insert_one({
        'categoryname': request.form['categoryname']
      })
      category = db.categories.find_one({'_id': created_category.inserted_id})

      return jsonify(json_encode(category))

    except:
      return {'message': 'An error occured'}, 500


  @staticmethod
  def update_category(db, id):
    try:
      updated_category = db.categories.update_one({'_id': ObjectId(id)}, {
        '$set': {
          'categoryname': request.form['categoryname']
        }
      })
      category = db.categories.find_one({'_id': ObjectId(id)})

      return jsonify(json_encode(category))

    except:
      return {'message': 'An error occured'}, 500
  
  @staticmethod
  def delete_category(db, id):
    try:
      updated_category = db.categories.delete_one({'_id': ObjectId(id)})

      return {
        'message': 'Deleted successfully'
      }
    
    except:
      return {'message': 'An error occured'}, 500