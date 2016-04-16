from src.models.model import Channel, ChannelUser, User


def leaderboard(**kwargs):
    channel = kwargs.get("channel")
    top_ten = ChannelUser.raw("""
        SELECT * FROM channelusers WHERE channel_id = ? ORDER BY points DESC LIMIT 10
    """, Channel.get(channel=channel).id)
    print [x for x in top_ten]
    resp = " | ".join([str(x[0] + 1) + ") " + User.get(
        id=x[1].username_id).username + " " + str(x[1].points) for x in enumerate(top_ten)])
    return resp
