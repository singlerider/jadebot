from src.lib.twitch import Twitch


def follower(args, **kwargs):
    username = args[0]
    channel = kwargs.get("channel", "testchannel")
    follower = Twitch(channel, username).follower_status()
    try:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                  "Sep", "Oct", "Nov", "Dec"]
        suffixes = ["st", "nd", "rd", "th",]
        date_split = follower["created_at"][:10].split("-")
        year = date_split[0]
        month = months[int(date_split[1]) - 1]
        day = date_split[2]
        if day[0] == "1":
            day = day + suffixes[3]
        elif day[1] == "1":
            day = day + suffixes[0]
        elif day[1] == "2":
            day = day + suffixes[1]
        elif day[1] == "3":
            day = day + suffixes[2]
        else:
            day = day + suffixes[3]
        follower_since = "{} {}, {}".format(month, day, year)
        return "{} has been following {} since {}.".format(username, channel, follower_since)
    except:
        return "{} doesn't follow {}.".format(username, channel)
