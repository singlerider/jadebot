from src.models.model import Channel, ChannelUser, User, db


def modify_points(channel, users, action, amount):
    channel = channel.lstrip("#")
    if action == "remove":
        amount = amount * -1
    with db.atomic():
        # creates a given channel entry if not exists
        Channel.get_or_create(channel=channel)
        for user in users:
            # creates a user entry if not exists
            User.get_or_create(username=user.lower())
            try:
                # attempts to retrieve a user object
                ChannelUser.get(
                    username=User.get(username=user.lower()).id,
                    channel=Channel.get(channel=channel).id)
            except ChannelUser.DoesNotExist:
                # if not exists, create channeluser object
                ChannelUser.create(username=User.get(
                    username=user.lower()).id, channel=Channel.get(
                        channel=channel).id)
            # update the channeluser object to an incremented amount
            ChannelUser.update(
                points=ChannelUser.points + amount
            ).where(
                ChannelUser.username == User.get(username=user.lower()).id,
                ChannelUser.channel == Channel.get(channel=channel).id
            ).execute()
    return
