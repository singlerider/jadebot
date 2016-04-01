from src.lib.twitch import Twitch
from datetime import datetime


def uptime(**kwargs):
    channel = kwargs.get("channel", "testchannel")
    format = "%Y-%m-%d %H:%M:%S"
    stream = Twitch(channel, None).stream()["stream"]
    if stream is not None:
        start_time = str(stream.get('created_at')).replace(
            "T", " ").replace("Z", "")
        stripped_start_time = datetime.strptime(start_time, format)
        time_delta = (datetime.utcnow() - stripped_start_time)
        return "The current !uptime is " + str(time_delta).split(".")[0]
    else:
        return channel + " is offline!"
