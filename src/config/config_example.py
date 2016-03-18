global config

channels_to_join = ['#singlerider']

for channel in channels_to_join:
    channel = channel.lstrip('#')

twitch_scopes = ["channel_subscriptions", "user_subscriptions"]

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
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
            # (60, True, pokemon.cron),  # pokemon released every 20 minutes
            # (600, True, treats.cron),  # treat handed out every 10 minutes
        ],
    },
}
