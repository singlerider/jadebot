import globals
import random


def drop(**kwargs):
    channel = kwargs.get("channel")
    username = kwargs.get("username")
    if username != "singlerider":
        return
    amount_to_divy = random.randint(20, 100)
    globals.CHANNEL_INFO[channel.lstrip("#")]["drop"] = {
        "amount": amount_to_divy,
        "active": True
    }
    response = "{0} ammo has just dropped! Be the first to \"!reload\"!".format(
        amount_to_divy)
    return response
