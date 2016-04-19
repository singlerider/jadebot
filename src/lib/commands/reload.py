import globals
from src.lib.points import modify_points


def reload(**kwargs):
    username = kwargs.get("username")
    channel = kwargs.get("channel")
    no_drop = "\'Looks like there isn't a drop right now!"
    if globals.CHANNEL_INFO[channel]["drop"].get("active") is True:
        amount = globals.CHANNEL_INFO[channel]["drop"]["amount"]
        modify_points(channel, [username], "add", amount)
        globals.CHANNEL_INFO[channel]["drop"]["amount"] = 0
        globals.CHANNEL_INFO[channel]["drop"]["active"] = False
        response = "{0} just reloaded and stocked up with {1} ammo!".format(
            username, amount)
        return response
    else:
        irc = kwargs.get("irc")
        irc.send_whisper(username, no_drop)
        return
