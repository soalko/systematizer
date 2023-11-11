import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_of_posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    posts_final = sqlalchemy.Column(sqlalchemy.String, nullable=False)
