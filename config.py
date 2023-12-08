import os
import dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = (f'postgresql://stupk:qwerty123@localhost:5432/finance'
    #                            or 'sqlite:///' + os.path.join(basedir, 'app.db'))
    PROPAGATE_EXCEPTIONS = True
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "Finance REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = ""

