class Config:
    DEBUG          = False
    TESTING        = False
    SECRET_KEY     = 'secret'
    DATABASEURL    = "sqlite:///db.sqlite"
    SHIPNAME       = ""
    REGISTRYNUMBER = ""

class Development(Config):
    DEBUG = True

class Production(Config):
    SECRET_KEY = 'an actually secret key'
