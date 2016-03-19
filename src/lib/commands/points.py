from src.models.model import User, Channel, ChannelUser, db


def cron(channel=None):
    from src.models.model import User, Channel, ChannelUser, db
    from src.lib.twitch import Twitch
    channel = channel.lstrip("#")
    __, all_users = Twitch(channel, None).users()
    with db.atomic():
        Channel.get_or_create(channel=channel)
        for user in all_users:
            User.get_or_create(username=user)
            try:
                ChannelUser.get(
                    username=User.get(username=user).id,
                    channel=Channel.get(channel=channel
                ).id)
            except ChannelUser.DoesNotExist:
                ChannelUser.create(username=User.get(
                    username=user).id, channel=Channel.get(channel=channel).id)
            ChannelUser.update(
                points=ChannelUser.points + 1,
                time_in_chat=ChannelUser.time_in_chat + 5
            ).where(
                ChannelUser.username == User.get(username=user).id,
                ChannelUser.channel == Channel.get(channel=channel).id
            ).execute()
    return


def points(args, **kwargs):
    username = kwargs.get("username")
    channel = kwargs.get("channel")
    if len(args) < 1:
        try:
            point_value = ChannelUser.get(
                username=User.get(username=username).id,
                channel=Channel.get(channel=channel).id).points
            time_value = ChannelUser.get(
                username=User.get(username=username).id,
                channel=Channel.get(channel=channel).id).time_in_chat
        except ChannelUser.DoesNotExist:
            point_value = 0
            time_value = 0
        except Exception as error:
            return error
        resp = "You have {0} points and have been watching for {1} minutes".format(
            point_value, time_value)
        return resp
    username = args[0]
    user, created = User.create_or_get(username=username)
    if created:
        return username + " added!"
    else:
        return username + " already exists!"
