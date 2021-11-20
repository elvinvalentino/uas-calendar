from utils.without_keys import without_keys


def json_encode(obj, keys = [], excludeKeys = []):
  obj['_id'] = str(obj['_id'])
  for key in keys:
    obj[key] = str(obj[key])
  
  return without_keys(obj, excludeKeys)