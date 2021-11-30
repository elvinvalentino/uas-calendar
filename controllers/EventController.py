from datetime import datetime
from flask import request, jsonify
from expetions.data import NotFound
from expetions.token import InvlidToken, NoToken
from utils.get_current_user import get_current_user
from utils.json_encode import json_encode
from bson.objectid import ObjectId


class EventController:
  @staticmethod
  def get_events(db):
    try:
      user = get_current_user(db)
      events = db.events.find({'userId': user['_id']})
      formattedEvents = [json_encode(event, ['userId', 'categoryId']) for event in events]
    
      return jsonify(refactor_get_events_response(db, formattedEvents))

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except:
      return {'message': 'An error occurred'}, 500

  @staticmethod
  def get_one_event(db, id):
    try:
      user = get_current_user(db)

      event = db.events.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if event is None:
        raise NotFound
      
      category = db.categories.find_one({'_id': event['categoryId']})

      formattedEvent = json_encode(event, ['userId', 'categoryId'])
      formattedEvent['category'] = json_encode(category, ['userId'])

      return jsonify(formattedEvent)
    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Event not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500
    

  @staticmethod
  def insert_event(db):
    try:
      user = get_current_user(db)

      category = db.categories.find_one({'_id': ObjectId(request.json['categoryId']), 'userId': user['_id']})
      if category is None:
        return {'message': 'Category not found'}

      created_event = db.events.insert_one({
        'userId': user['_id'],
        'categoryId': category['_id'],
        'title':request.json['title'],
        'description':request.json['description'],
        'type':request.json['type'],
        'dateStart': datetime.strptime(request.json['dateStart'], '%Y-%m-%d %I:%M%z'),
        'dateEnd':datetime.strptime(request.json['dateEnd'], '%Y-%m-%d %I:%M%z'),
        'duration': int(request.json['duration']),
        'isAllDay':True if request.json['isAllDay'] == 'true' else False,
        'isDone':True if request.json['isDone'] == 'true' else False,
      })
      event = db.events.find_one({'_id': created_event.inserted_id})

      formattedEvent = json_encode(event, ['userId', 'categoryId'])
      formattedEvent['category'] = json_encode(category, ['userId'])

      return jsonify(formattedEvent)

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Event not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500


  @staticmethod
  def update_event(db, id):
    try:
      user = get_current_user(db)

      event = db.events.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if event is None:
        raise NotFound

      category = db.categories.find_one({'_id': ObjectId(request.json['categoryId']), 'userId': user['_id']})
      if category is None:
        return {'message': 'Category not found'}

      db.events.update_one({'_id': ObjectId(id)}, {
        '$set': {
          'userId': user['_id'],
          'categoryId':category['_id'],
          'title':request.json['title'],
          'description':request.json['description'],
          'type':request.json['type'],
          'dateStart':datetime.strptime(request.json['dateStart'], '%Y-%m-%d %I:%M%z'),
          'dateEnd':datetime.strptime(request.json['dateEnd'], '%Y-%m-%d %I:%M%z'),
          'isAllDay':True if request.json['isAllDay'] == 'true' else False,
          'isDone':True if request.json['isDone'] == 'true' else False,
        }
      })

      event = db.events.find_one({'_id': ObjectId(id)})
      
      formattedEvent = json_encode(event, ['userId', 'categoryId'])
      formattedEvent['category'] = json_encode(category, ['userId'])

      return jsonify(formattedEvent)

    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Event not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500
  
  @staticmethod
  def delete_event(db, id):
    try:
      user = get_current_user(db)

      event = db.events.find_one({'_id': ObjectId(id), 'userId': user['_id']})
      if event is None:
        raise NotFound

      db.events.delete_one({'_id': ObjectId(id)})

      return {
        'message': 'Deleted successfully'
      }
    except NoToken:
      return {'message': 'No Token Provided'}, 400
    except InvlidToken:
      return {'message': 'Invalid Token'}, 400
    except NotFound:
      return {'message': 'Event not found'}, 404
    except:
      return {'message': 'An error occurred'}, 500

def refactor_get_events_response(db, events):
    result = []
    for event in events:
      category = db.categories.find_one({'_id': ObjectId(event['categoryId'])})
      event['category'] = json_encode(category, ['userId'])
      result.append(event)

    return result