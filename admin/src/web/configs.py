import os
from os import environ
from datetime import timedelta
class Config(object):
    '''Base configuracion'''

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    JWT_SECRET_KEY = "secret_key"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Reemplaza con tu servidor SMTP
    MAIL_PORT =  465  #app.config[ Puerto SMTP (generalmente 587 para TLS)
    MAIL_USERNAME = 'valentindome777@gmail.com'  # Tu dirección de correo electrónico
    MAIL_PASSWORD = 'cvpk mipr lqzn kgdq'  # Tu contraseña de correo electrónico
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # Configuración de Google para autenticación
    GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID')
    # GOOGLE_CLIENT_ID = os.getenv('193229960820-ruljkn9bnh3rjftm5b0a0q9840rrtp9v.apps.googleusercontent.com')
    # GOOGLE_CLIENT_SECRET = os.getenv('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')


class ProductionConfig(Config):
    '''Producto Configuration'''
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    '''Development Configuration'''

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")


    # DB_USER = "postgres"
    # DB_PASS = "postgres"
    # DB_HOST = "localhost"
    # DB_NAME = "grupo24"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )



class TestingConfig(Config):
    '''Testing Configuration'''
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "mantenimiento": False,
    "cantRegPags": 5,
    "inf_contacto": "Para comunicarse con nosotros llamenos 221-2211222 o al email cidepint@hotmail.com"
}
