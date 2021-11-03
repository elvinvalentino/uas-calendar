from flask import request, jsonify
from markupsafe import escape
from utils.json_encode import json_encode
from bson.objectid import ObjectId


class EventController:
  @staticmethod
  def get_events(db):
    try:
      events = db.events.find()
      response = []
    
      return jsonify([json_encode(event) for event in events])

    except:
      return {'message': 'An error occured'}, 500

  @staticmethod
  def get_one_event(db, id):
    try:
      event = db.events.find_one({'_id': ObjectId(id)})
      return jsonify(json_encode(event))
    except:
      return {'message': 'An error occured'}, 500
    

  @staticmethod
  def insert_event(db):
    try:
      created_event = db.events.insert_one({
        'eventname': request.form['eventname']
      })
      event = db.events.find_one({'_id': created_event.inserted_id})

      return jsonify(json_encode(event))

    except:
      return {'message': 'An error occured'}, 500


  @staticmethod
  def update_event(db, id):
    try:
      updated_event = db.events.update_one({'_id': ObjectId(id)}, {
        '$set': {
          'eventname': request.form['eventname']
        }
      })
      event = db.events.find_one({'_id': ObjectId(id)})

      return jsonify(json_encode(event))

    except:
      return {'message': 'An error occured'}, 500
  
  @staticmethod
  def delete_event(db, id):
    try:
      updated_event = db.events.delete_one({'_id': ObjectId(id)})

      return {
        'message': 'Deleted successfully'
      }
    
    except:
      return {'message': 'An error occured'}, 500