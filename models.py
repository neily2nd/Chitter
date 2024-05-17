# models.py
import datetime
from peewee import *


# Define database connection
db = SqliteDatabase('chitter.db')

# Define User model
class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    name = CharField()

    class Meta:
        database = db

# Define Peep model
class Peep(Model):
    user = ForeignKeyField(User, backref='peeps')
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
