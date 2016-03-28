from src.models.model import Channel, User, Command, db
from src.lib.command_headers import commands


def add(
        channel, username, trigger, response, user_level, time_interval,
        times_used):
    channel = channel.lstrip("#")
    if commands.get(trigger) is not None:
        return "{0} is already a builtin command in {1}!".format(
            trigger, channel)
    with db.atomic():
        User.get_or_create(username=username)
        Channel.get_or_create(channel=channel)
        try:
            # attempts to retrieve a user object
            Command.get(
                channel=Channel.get(channel=channel).id,
                trigger=trigger)
            return "{0} already exists in {1}!".format(trigger, channel)
        except Command.DoesNotExist:
            # if not exists, create channeluser object
            Command.create(
                username=User.get(username=username).id,
                channel=Channel.get(channel=channel).id,
                trigger=trigger, response=response, user_level=user_level,
                time_interval=time_interval, time_used=0)


def edit(
        channel, username, trigger, response, user_level, time_interval,
        times_used):
    channel = channel.lstrip("#")
    if commands.get(trigger) is not None:
        return "{0} can't be edited in {1}!".format(
            trigger, channel)
    with db.atomic():
        User.get_or_create(username=username)
        Channel.get_or_create(channel=channel)
        try:
            # attempts to retrieve a user object
            Command.get(
                channel=Channel.get(channel=channel).id,
                trigger=trigger)
            Command.update.(
                username=User.get(username=username).id,
                trigger=trigger, response=response, user_level=user_level,
                time_interval=time_interval
                ).where(
                    channel=Channel.get(channel=channel).id,
                    trigger=trigger
                ).execute()
        except Command.DoesNotExist:
            return "{0} not found in {1}!".format(trigger, channel)


def remove(channel, trigger):
    channel = channel.lstrip("#")
    if commands.get(trigger) is not None:
        return "{0} can't be deleted from {1}!".format(trigger, channel)
    with db.atomic():
        try:
            # attempts to retrieve a user object
            Command.get(
                channel=Channel.get(channel=channel).id,
                trigger=trigger)
            Command.delete().where(
                channel=Channel.get(channel=channel).id,
                trigger=trigger
            ).execute()
        except Command.DoesNotExist:
            return "{0} not found in {1}!".format(trigger, channel)


def get(channel, username, trigger):
    channel = channel.lstrip("#")
    with db.atomic():
        try:
            command = Command.get(
                channel=Channel.get(channel=channel).id,
                trigger=trigger)
            return command
        except Command.DoesNotExist:
            return None
