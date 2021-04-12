import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class PLayer(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    played_games = sqlalchemy.Column(sqlalchemy.Integer, default=0)