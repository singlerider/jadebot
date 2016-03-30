from src.models.model import User, Channel, Command, db


def add(args, **kwargs):
    username = kwargs.get("username")
    channel = kwargs.get("channel")
    args = args[0].split(" ")
    trigger = args[0]
    user_level = args[1]
    if user_level != "reg" and user_level != "mod":
        return "user_level must be \"reg\" or \"mod\""
    response = " ".join(args[2:])
    if response.startswith("/w"):
        return "response can't be a whisper"
    with db.atomic():
        try:
            # attempts to retrieve a user object
            Command.get(channel=Channel.get(
                channel=channel).id, trigger=trigger.lstrip("!"))
            return "{0} already exists".format(trigger)
        except Command.DoesNotExist:
            User.get_or_create(username=username)
            Channel.get_or_create(channel=channel)
            Command.create(
                username=User.get(username=username).id,
                channel=Channel.get(channel=channel).id,
                trigger=trigger.lstrip("!"), response=response, user_level=user_level,
                times_used=0)
    return "{0} created".format(trigger)
