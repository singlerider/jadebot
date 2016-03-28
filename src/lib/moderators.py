from src.models.model import ChannelUser, Channel, User


def add_moderator(channel, user):
    channel = channel.lstrip("#")
    ChannelUser.update(
        is_moderator=1
    ).where(
        ChannelUser.username == User.get(username=user).id,
        ChannelUser.channel == Channel.get(channel=channel).id,
        ChannelUser.is_moderator == 0
    ).execute()


def get_moderator(channel, user):
    channel = channel.lstrip("#")
    try:
        # attempts to retrieve a user object
        is_mod = ChannelUser.get(
            username=User.get(username=user).id,
            channel=Channel.get(channel=channel).id).is_moderator
        return is_mod
    except ChannelUser.DoesNotExist:
        # if not exists, create channeluser object
        is_mod = None
        return is_mod
