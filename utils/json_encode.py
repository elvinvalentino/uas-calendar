def json_encode(obj):
  obj['_id'] = str(obj['_id'])
  return obj