from project import app
import sqlalchemy as sa
import sqlalchemy.orm as so
from project import app, db
from project.models import UserModel, RecordModel, CategoryModel


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'UserModel': UserModel, 'RecordModel': RecordModel,
            'CategoryModel': CategoryModel}
