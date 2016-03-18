from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('db.sqlite3')


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, null=False)
    created_at = DateTimeField(default=datetime.datetime.now)


class Channel(BaseModel):
    channel = CharField(unique=True, null=False)
    twitch_auth = CharField(default=None)
    twitchalerts_auth = CharField(default=None)
    streamtip_auth = CharField(default=None)
    created_at = DateTimeField(default=datetime.datetime.now)


class ChannelUser(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    created_at = DateTimeField(default=datetime.datetime.now)
    points = IntegerField(null=False)
    time_in_chat = IntegerField(null=False)
    is_moderator = BooleanField(default=False)


class Command(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    created_at = DateTimeField(default=datetime.datetime.now)
    trigger = CharField(null=False)
    response = CharField(null=False)
    user_level = BooleanField(null=False)
    time_interval = IntegerField(null=False)
    last_triggered = DateTimeField(default=datetime.datetime.now)
    times_used = IntegerField(null=False)


class Quote(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    created_at = DateTimeField(default=datetime.datetime.now)
    message = CharField(null=False)
    game = CharField(null=False)

db.connect()
db.create_tables([User, Channel, ChannelUser, Command, Quote])
