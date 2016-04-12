from src.lib.twitch import Twitch


def followers(**kwargs):
    username = kwargs.get("username", "testuser")
    channel = kwargs.get("channel", "testchannel")
    stream_followers = Twitch(channel, username).followers()
    follower_list = str(
        stream_followers["follows"][0]["user"]["display_name"]) + ", " + str(
        stream_followers["follows"][1]["user"]["display_name"]) + ", " + str(
            stream_followers["follows"][2]["user"]["display_name"]) + ", " + str(
                stream_followers["follows"][3]["user"]["display_name"]) + ", " + str(
                    stream_followers["follows"][4]["user"]["display_name"])
    resp = "Most recent followers: " + follower_list + ". "
    return resp
