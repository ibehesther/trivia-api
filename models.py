from email.policy import default
import os
from os.path import join, dirname
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

database_path = 'postgresql://{}:{}@{}/{}'.format(
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME)

db = SQLAlchemy()


# """
# setup_db(app)
#     binds a flask application and a SQLAlchemy service
# """
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=True, default=1)

    def __init__(self, question, answer, category, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty,
            'rating': self.rating
            }

    def __repr__(self):
        return f'<id: {self.id}, category: {self.category}>'


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }

    def __repr__(self):
        return f'< id: {self.id}, type: {self.type} >'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True, default='Anon')
    score = db.Column(db.Integer, nullable=True, default=0)

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'< id: {self.id}, name: {self.name}, score: {self.score} >'
