from flask import Flask
from flask_smorest import Api
from resources import user, category, record

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

api.register_blueprint(user.blp)
api.register_blueprint(category.blp)
api.register_blueprint(record.blp)

from project import views, models

