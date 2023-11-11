import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Students(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    in_plan = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
