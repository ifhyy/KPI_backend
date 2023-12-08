from datetime import datetime

from project import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm


class UserModel(db.Model):
    __table_name__ = "user"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    records: orm.WriteOnlyMapped['RecordModel'] = orm.relationship('RecordModel', backref='user')


class CategoryModel(db.Model):
    __table_name__ = "category"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    category_name: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    records: orm.WriteOnlyMapped['RecordModel'] = orm.relationship('RecordModel', backref='category')


class RecordModel(db.Model):
    __table_name__ = "record"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey(UserModel.id), index=True)
    category_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey(CategoryModel.id), index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(),
                                                         nullable=False)

    user: orm.Mapped[UserModel] = orm.relationship('UserModel', backref='records')
    category: orm.Mapped[CategoryModel] = orm.relationship('CategoryModel', backref='records')

    
