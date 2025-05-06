from quart import current_app
from quart import session
from quart import abort

from jose import jwt

def require_role(*roles_required):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                token = jwt.get_unverified_claims(session['auth_token']['access_token'])
                if set(roles_required).issubset(token['groups']):
                    return await func(*args, **kwargs)
                else:
                    abort(403)
            else:
                abort(401)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

def require_login(func):
    async def wrapper(*args, **kwargs):
        if 'auth_token' in session:
            return await func(*args, **kwargs)
        else:
            abort(401)
    wrapper.__name__ = func.__name__
    return wrapper

def authorize_action(func):
    async def wrapper(*args,**kwargs):
        if 'auth_token' in session:
            #TODO: implement jwt encoding for the request
            #TODO: implement jwt send
            #TODO: implement response wait and decode
            pass
        else:
            abort(401)
    wrapper.__name__ = func.__name__
    return wrapper
