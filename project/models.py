from datetime import datetime

from project.db import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm


class UserModel(db.Model):
    __table_name__ = "user"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    account: orm.Mapped["AccountModel"] = orm.relationship(back_populates='owner')


class CategoryModel(db.Model):
    __table_name__ = "category"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    category: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    # records: orm.WriteOnlyMapped['RecordModel'] = orm.relationship('RecordModel', backref='category')


class RecordModel(db.Model):
    __table_name__ = "record"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey(UserModel.id), index=True)
    category_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey(CategoryModel.id), index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(),
                                                         nullable=False)
    sum: orm.Mapped[float] = orm.mapped_column(sa.Float(precision=2), unique=False, nullable=False)

    user: orm.Mapped[UserModel] = orm.relationship('UserModel', backref='records')
    category: orm.Mapped[CategoryModel] = orm.relationship('CategoryModel', backref='records')


class AccountModel(db.Model):
    __table_name__ = "account"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    owner_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey(UserModel.id), index=True, unique=True)
    net_worth: orm.Mapped[float] = orm.mapped_column(sa.Float(precision=2), unique=False, default=0)

    owner: orm.Mapped[UserModel] = orm.relationship('UserModel', back_populates='account', single_parent=True)

