from src.lib.points import modify_points


def donation(args, **kwargs):
    user = args[0].lower().lstrip("@")
    channel = kwargs.get("channel")
    amount = args[1]
    try:
        amount = int(float(amount.lstrip(u"\u00a3")))
    except Exception as error:
        print error
        return "amount has to be a number, ya dingus!"
    ammo_to_add = abs(int(amount / 5) * 500)
    modify_points(channel, [user], "add", ammo_to_add)
    thanks_message = u"Let's get some jadeHype in the chat for {0}'s \u00a3{1} donation!".format(
        user, amount)
    if ammo_to_add < 5:
        return thanks_message
    else:
        return "{} ammo for {}! {}".format(ammo_to_add, user, thanks_message)
