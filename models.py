import datetime
from peewee import *

DATABASE = SqliteDatabase('database/main.db')


class BaseModel (Model):
    class Meta:
        database = DATABASE


class User (BaseModel):
    email = CharField(unique=True)
    password = CharField()


""" class Message (BaseModel):
    user_id = ForeignKeyField(User, backref='messages')
    content = TextField()
    published_at = DateTimeField(default=datetime.datetime.now()) """


class Article (BaseModel):
    user_id = ForeignKeyField(User, backref='articles')
    title = TextField()
    description = TextField()
    published_at = DateTimeField(default=datetime.datetime.now())


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Article], safe=True)
    DATABASE.close()
