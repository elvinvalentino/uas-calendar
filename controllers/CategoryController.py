from flask import request, jsonify
from markupsafe import escape
from expetions.data import NotFound
from expetions.token import InvlidToken, NoToken
from utils.get_current_user import get_current_user
from utils.json_encode import json_encode
from bson.objectid import ObjectId


class CategoryController:
  @staticmethod
  def get_categories(db):
    try:
      user = get_current_user(db)

      categories = db.categories.find({'userId': user['_id']})
      return jsonify([json_encode(category, ['userId']) for category in categories])

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except:
      return {'message': 'An error occurred'}, 500

  @staticmethod
  def get_one_category(db, id):
    try:
      user = get_current_user(db)

      category = db.categories.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if category is None:
        raise NotFound

      return jsonify(json_encode(category, ['userId']))
    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Category not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500
    

  @staticmethod
  def insert_category(db):
    try:
      user = get_current_user(db)

      created_category = db.categories.insert_one({
        'userId':user['_id'],
        'name': request.form['name'],
        'hex':request.form['hex'],
        'isPreset': False
      })
      category = db.categories.find_one({'_id': created_category.inserted_id})

      return jsonify(json_encode(category, ['userId']))

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except:
      return {'message': 'An error occurred'}, 500


  @staticmethod
  def update_category(db, id):
    try:
      user = get_current_user(db)

      category = db.categories.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if category is None:
        raise NotFound

      db.categories.update_one({'_id': ObjectId(id)}, {
        '$set': {
          'name': request.form['name'],
          'hex':request.form['hex']
        }
      })
      category = db.categories.find_one({'_id': ObjectId(id)})

      return jsonify(json_encode(category, ['userId']))

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Category not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500
  
  @staticmethod
  def delete_category(db, id):
    try:
      user = get_current_user(db)

      category = db.categories.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if category is None:
        raise NotFound

      defaultCategory = db.categories.find_one({'userId': user['_id'], 'isPreset': True})

      db.events.update_many({'category_id': category['_id']}, {
        '$set': {
          'categoryId': defaultCategory['_id'],
        }
      })

      db.categories.delete_one({'_id': ObjectId(id)})
      return {
        'message': 'Deleted successfully'
      }

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Category not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500