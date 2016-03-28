import src.lib.commands.points as points
global config

channels_to_join = ['#singlerider']

for channel in channels_to_join:
    channel = channel.lstrip('#')

twitch_scopes = ["channel_subscriptions", "user_subscriptions"]

config = {
    # details required to login to twitch IRC server
    'superuser': 'singlerider',
    'extra_channel': '#singlerider',
    'test_user': 'duck__butter',
    'username': 'JadeBot',
    # get this from http://twitchapps.com/tmi/
    'oauth_password': 'oauth:6yc3lsd1ho0jmw52vr58udcy2mqe32',

    'debug': True,
    'log_messages': True,

    'channels': channels_to_join,

    # Cron jobs.
    'cron': {
        '#singlerider': [
            # time, run, callback
            (15, True, points.cron)  # treat handed out every 10 minutes
            # (60, True, pokemon.cron),  # pokemon released every 20 minutes
            # (600, True, treats.cron),
        ],
    },
}
