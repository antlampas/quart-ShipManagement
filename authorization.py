from quart import session
from quart import redirect
from quart import url_for
from quart import abort

from jose  import jwt
import json

def require_role(*roles):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                token = jwt.get_unverified_claims(session['auth_token']['access_token'])
                if 'realm_access' in token and 'roles' in token['realm_access'] and set(roles).issubset(token['realm_access']['roles']):
                    return await func(*args, **kwargs)
                else:
                    abort(403)
            else:
                abort(401)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
