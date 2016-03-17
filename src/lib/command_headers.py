commands = {
    '!report': {
        'limit': 200,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'ul': 'mod',
        'usage': "!report [insert bug report text here]"
    },
    '!commands': {
        'limit': 10,
        'argc': 0,
        'return': 'command',
        'usage': '!commands'
    },
    '!opinion': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'ul': 'reg',
        'usage': '!opinion',
        'user_limit': 30
    },
    # '!llama': {
    #     'limit': 0,
    #     'argc': 1,
    #     'return': 'command',
    #     'usage': "!llama ['treats'/'shots'/username/'list']",
    #     'optional': True,
    #     'user_limit': 30
    # },
    # '!treats': {
    #     'limit': 0,
    #     'return': 'command',
    #     'argc': 3,
    #     'ul': 'mod',
    #     'usage': '!treats [add/remove/set] [username] [number]'
    # },
    '!help': {
        'limit': 15,
        'return': 'There is a super useful README for the bot at  at github.com/singlerider/PLACEHOLDER',
        'usage': '!help',
        'user_limit': 30
    },
    '!followers': {
        'limit': 30,
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
        'ul': 'mod'
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
    '!define': {
        'limit': 30,
        'user_limit': 300,
        'argc': 1,
        'space_case': True,
        'return': 'command',
        'usage': '!define [insert_word_here]'
    },
    '!caster': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!caster [streamer_username]',
        'ul': 'mod'
    },
    '!donation': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!donation [username] [dollar_amount]',
        'ul': 'mod'
    },
    '!add': {
        'limit': 0,
        'argc': 4,
        'return': 'command',
        'usage': '!add [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}") (to include message count, use "[]")]',
        'ul': 'mod'
    },
    '!rem': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!rem [!command_name]',
        'ul': 'mod'
    },
    '!edit': {
        'limit': 0,
        'argc': 4,
        'return': 'command',
        'usage': '!edit [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}")]',
        'ul': 'mod'
    },
    '!weather': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!weather [units (metric/imperial)] [location (any format)]',
        'ul': 'mod'
    },
    '!addquote': {
        'limit': 0,
        'argc': 1,
        'user_limit': 15,
        'return': 'command',
        'usage': '!addquote [quote]',
        'space_case': True
    },
    '!quote': {
        'limit': 0,
        'argc': 0,
        'user_limit': 5,
        'return': 'command',
        'usage': '!quote'
    },
    '!subcount': {
        'limit': 0,
        'argc': 0,
        'ul': 'mod',
        'return': 'command',
        'usage': '!subcount'
    },
}

user_cooldowns = {"channels": {}}


def initalizeCommands(config):
    for channel in config['channels']:
        user_cooldowns["channels"][channel] = {"commands": {}}
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}

if __name__ == "__main__":  # pragma: no cover
    print "\n".join(["    " + key + ": " + commands[key][
        "usage"] for key in commands])