import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    floor = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    am_m = sqlalchemy.Column(sqlalchemy.Integer)
    am_f = sqlalchemy.Column(sqlalchemy.Integer)
