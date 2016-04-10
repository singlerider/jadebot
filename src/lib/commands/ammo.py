from src.lib.points import modify_points
from src.models.model import Channel, ChannelUser, User


def cron(channel=None):
    import globals
    from src.models.model import User, Channel, ChannelUser, db
    from src.lib.twitch import Twitch
    from src.lib.moderators import add_moderator
    channel = channel.lstrip("#")
    try:
        if Twitch(channel, None).stream().get("stream") is None:
            globals.CHANNEL_INFO[channel.lstrip("#")]["online"] = False
            return
        globals.CHANNEL_INFO[channel.lstrip("#")]["online"] = True
        user_dict, all_users = Twitch(channel, None).users()
        with db.atomic():
            # creates a given channel entry if not exists
            Channel.get_or_create(channel=channel)
            for user in all_users:
                # creates a user entry if not exists
                User.get_or_create(username=user)
                try:
                    # attempts to retrieve a user object
                    ChannelUser.get(
                        username=User.get(username=user).id,
                        channel=Channel.get(channel=channel).id)
                except ChannelUser.DoesNotExist:
                    # if not exists, create channeluser object
                    ChannelUser.create(username=User.get(
                        username=user).id, channel=Channel.get(channel=channel).id)
                # update the channeluser object to an incremented amount
                ChannelUser.update(
                    points=ChannelUser.points + 1,
                    time_in_chat=ChannelUser.time_in_chat + 5
                ).where(
                    ChannelUser.username == User.get(username=user).id,
                    ChannelUser.channel == Channel.get(channel=channel).id
                ).execute()
        for user in user_dict["chatters"]["moderators"]:
            add_moderator(channel, user)
        return
    except:
        pass


def drop(channel=None):
    import time
    import random
    import globals
    time_to_sleep = random.randint(1, 1500)
    amount_to_divy = random.randint(20, 100)
    time.sleep(time_to_sleep)
    try:
        if globals.CHANNEL_INFO[channel.lstrip("#")]["online"] is True:
            print "TRUE"
            globals.CHANNEL_INFO[channel.lstrip("#")]["drop"] = {
                "amount": amount_to_divy,
                "active": True
            }
            response = "{0} ammo has just dropped! Be the first to \"!reload\"!".format(amount_to_divy)
            return response
        else:
            globals.CHANNEL_INFO[channel.lstrip("#")]["drop"] = {
                "amount": 0,
                "active": False
            }
    except:
        pass



def ammo(args, **kwargs):
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
        resp = "You have {0} ammo and have been watching for {1} minutes".format(
            point_value, time_value)
        return resp
    if len(args) == 1:
        user_to_check = args[0].lower()
        User.get_or_create(username=user_to_check)
        try:
            point_value = ChannelUser.get(
                username=User.get(username=user_to_check).id,
                channel=Channel.get(channel=channel).id).points
            time_value = ChannelUser.get(
                username=User.get(username=user_to_check).id,
                channel=Channel.get(channel=channel).id).time_in_chat
        except ChannelUser.DoesNotExist:
            resp = "{0} not found".format(user_to_check)
            return resp
        except Exception as error:
            return error
        resp = "{0} has {1} ammo and has been watching for {2} minutes".format(
            user_to_check, point_value, time_value)
        return resp
    if len(args) == 3:
        action = args[0]
        username_to_modify = args[1].lower()
        amount = args[2]
        try:
            amount = int(amount)
        except:
            return "Amount must be a number."
        if action == "add" or action == "remove":
            modify_points(channel, [username_to_modify], action, amount)
            return (
                str(amount) + " ammo " + action.rstrip("e") + "ed on " +
                username_to_modify + "!")
        else:
            return "Action must be \"add\" or \"remove\"."
    else:
        return "\"!ammo\" takes either 0, 1, or 3 arguments."
