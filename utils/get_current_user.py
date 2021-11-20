from flask import request

from expetions.token import InvlidToken, NoToken

def get_current_user(db):
  token = request.args.get('token')
  if token is None:
    raise NoToken()

  user = db.users.find_one({'accessToken': token})
  if user is None:
    raise InvlidToken()

  return user
