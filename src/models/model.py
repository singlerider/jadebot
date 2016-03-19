from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase("db.sqlite3")


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, null=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "users"


class Channel(BaseModel):
    channel = CharField(unique=True, null=False)
    twitch_auth = CharField(default="")
    twitchalerts_auth = CharField(default="")
    streamtip_auth = CharField(default="")
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "channels"


class ChannelUser(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    points = IntegerField(default=0)
    time_in_chat = IntegerField(default=0)
    is_moderator = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "channelusers"


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

    class Meta:
        db_table = "commands"


class Quote(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    created_at = DateTimeField(default=datetime.datetime.now)
    message = CharField(null=False)
    game = CharField(null=False)

    class Meta:
        db_table = "quotes"


class Message(BaseModel):
    username = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    message = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "messages"

try:
    db.connect()
    db.create_tables([User, Channel, ChannelUser, Command, Quote, Message])
except OperationalError:
    pass
