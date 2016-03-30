from src.models.model import Channel, Command, db


def rem(args, **kwargs):
    channel = kwargs.get("channel")
    trigger = args[0].lstrip("!").lower()
    with db.atomic():
        try:
            # attempts to retrieve a user object
            Command.get(channel=Channel.get(
                channel=channel).id, trigger=trigger)
            Command.delete().where(
                Command.trigger == trigger,
                Command.channel == Channel.get(channel=channel).id).execute()
        except Command.DoesNotExist:
            return "{0} does not exist".format(trigger)
    return "{0} removed".format(trigger)
