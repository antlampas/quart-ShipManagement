from quart import current_app
from quart import session
from quart import abort

from typing import overload

from jose import jwt

def require_role(*requiredRoles):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                token = jwt.get_unverified_claims(session['auth_token']['access_token'])
                userRoles = token['groups']
                numberOfRequiredRoles = len(userRoles)
                rolesMatched = 0
                for requiredRole in requiredRoles:
                    for userRole in userRoles:
                        if requiredRole in userRole:
                            rolesMatched += 1
                if rolesMatched == numberOfRequiredRoles:
                    return await func(*args, **kwargs)
                else:
                    abort(403)
            else:
                abort(401)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@overload
def require_user(requiredUsername):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                token = jwt.get_unverified_claims(session['auth_token']['access_token'])
                if token['preferred_username'] == requiredUsername:
                    return await func(*args, **kwargs)
                else:
                    abort(403)
            else:
                abort(401)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@overload
def require_user(requiredUsername):
    if 'auth_token' in session:
        token = jwt.get_unverified_claims(session['auth_token']['access_token'])
        if token['preferred_username'] == requiredUsername:
            return True
        else:
            abort(403)
    else:
        abort(401)

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
