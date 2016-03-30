from src.models.model import Channel, Command, db


def edit(args, **kwargs):
    channel = kwargs.get("channel")
    args = args[0].split(" ")
    print args
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
                channel=channel).id, trigger=trigger.lstrip("!"),
                user_level=user_level)
            Command.update(response=response).where(
                Command.channel == Channel.get(channel=channel).id,
                Command.trigger == trigger
            ).execute()
        except Command.DoesNotExist:
            return "{0} not found".format(trigger)
    return "{0} modified".format(trigger)
