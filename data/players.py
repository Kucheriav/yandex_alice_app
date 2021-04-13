import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    played_games = sqlalchemy.Column(sqlalchemy.Integer, default=0)