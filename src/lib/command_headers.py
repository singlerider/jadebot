import globals

commands = {
    '!report': {
        'limit': 200,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'user_level': 'mod',
        'usage': "!report [insert bug report text here]"
    },
    '!opinion': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'user_level': 'reg',
        'usage': '!opinion',
        'user_limit': 30
    },
    '!ammo': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': "!ammo *['add'/'remove'] [username] [amount]",
        'optional': True,
        'user_limit': 30,
        'user_level': 'mod'
    },
    '!help': {
        'limit': 15,
        'return': 'There is a super useful README for the bot at  at github.com/singlerider/jadebot',
        'usage': '!help',
        'user_limit': 30
    },
    '!followers': {
        'limit': 30,
        'user_level': 'mod',
        'return': 'command',
        'argc': 0,
        'usage': '!followers',
        'user_limit': 30,
    },
    '!follower': {
        'limit': 0,
        'return': 'command',
        'argc': 1,
        'usage': '!follower [username]',
        'user_level': 'mod'
    },
    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime',
        'user_limit': 30,
    },
    '!stream': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!stream'
    },
    '!winner': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!winner',
        'user_limit': 30,
    },
    '!popularity': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'usage': '!popularity [name_of_game]'
    },
    '!caster': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!caster [streamer_username]',
        'user_level': 'mod'
    },
    '!donation': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!donation [username] [currency_amount]',
        'user_level': 'mod'
    },
    '!reload': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!reload'
    },
    '!drop': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!drop'
    },
    '!leaderboard': {
        'limit': 300,
        'argc': 0,
        'return': 'command',
        'usage': '!leaderboard',
        'user_level': 'mod'
    }
}

user_cooldowns = {"channels": {}}


def initalizeCommands(config):
    for channel in config['channels']:
        globals.CHANNEL_INFO[channel.lstrip("#")] = {"drop": {}}
        user_cooldowns["channels"][channel] = {"commands": {}}
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}

if __name__ == "__main__":  # pragma: no cover
    print "{\n" + ",\n".join(["    \"" + key + "\": \"" + commands[key][
        "usage"] for key in commands]) + "\"\n}"
