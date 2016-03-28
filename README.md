Try it out! The Code is live at [http://www.twitch.tv/jadejolie](http://www.twitch.tv/jadejolie) You can send a whisper by typing `/w Jadebot hi` into the chat (from any channel)!

# Jadebot
A bot with personality

Introducing Jadebot - a Twitch chat/irc bot written in `Python` (2.6 / 2.7) with **FULL WHISPER SUPPORT** and more features than I care to count at this point. This implementation relies on a highly customized IRC connection library that allows for hot event-driven bot action over multiple sockets at once.

## Installation
### Virtual Environment
I would recommend running this in a virtual environment to keep your dependencies in check. If you'd like to do that, run:

```shell
sudo pip install virtualenv
```

Followed by:

```shell
virtualenv venv
```

This will create an empty virtualenv in your project directory in a folder called "venv." To enable it, run:

```shell
source venv/bin/activate
```

and your console window will be in that virtualenv state. To deactivate, run:

```shell
deactivate
```

### Dependencies
To install all dependencies locally (preferably inside your activated virtualenv), run:

```shell
pip install -r requirements.txt
```

### Further Steps
Make a copy of the example config file:

```shell
cp src/config/config_example.py src/config/config.py
```

Make a copy of the example globals file:

```shell
cp globals_example.py globals.py
```

Create a user that you will use to connect with the database with (you do not want to connect as root for security reasons) - replace "newuser" and "password" with whatever you'd like:

Create your schema from my blank template:

#### Globals and Config Files
Head into `src/config/config.py` and enter the correct channels and cron jobs you'd like to run, then go into `globals.py`. Leave `VARIABLE`, and `CHANNEL_INFO` alone.

## Finally
### To run:

```shell
./serve.py
```

## Commands
So, what can the bot do? Here are a list of current commands in no particular order with a description of each (if one is needed):

```
!follower: !follower [username]
!winner: !winner
!add: !add [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}") (to include message count, use "[]")]
!opinion: !opinion
!donation: !donation [username] [dollar_amount]
!quote: !quote
!commands: !commands
!rem: !rem [!command_name]
!addquote: !addquote [quote]
!uptime: !uptime
!caster: !caster [streamer_username]
!define: !define [insert_word_here]
!edit: !edit [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}")]
!followers: !followers
!subcount: !subcount
!help: !help
!popularity: !popularity [name_of_game]
!report: !report [insert bug report text here]
!weather: !weather [units (metric/imperial)] [location (any format)]
!stream: !stream
!points: !points *['add'/'remove'] [username] [amount]
```

## Make It Do
### Adding your own commands
You're going to need to know basic Python if you want to add your own commands. Open up `src/lib/command_headers.py`. There are examples of pre-made commands in there as examples. The limit parameter is the amount of times a command can be used in seconds, if you don't want a limit to be enforced put in `0`.

The `'limit'` parameter is the amount of times a command can be used in seconds, if you don't want a limit to be enforced put in `0`.

If your command is only going to return a string, ex - `'!hello'` returns `'Welcome!'`, don't include the `'argc'` parameter. Place the string you wish to be returned to the user in the `'return'` parameter. For example, if you wanted to create a command such as this and limit it to being used ever 30 seconds, you would add in:

```python
'!hello': {
    'limit': 10,
    'return': 'Welcome!'
}
```

However, if your command has to have some logic implemented and if the command is just going to return whatever a function returns, set the `'return'` parameter on the command to `'command'`, and set `'argc'` to `0`. If your command is going to take arguments, ex `'!hello [name]'`, set `'argc'` to `'1'` or however many arguments the command is going to take in.

Make a new file in `'lib/commands/'` and give the filename `'command.py'` where `command` is the command name. If your `'argc'` was set to `0`, don't include `'args'` in the functions parameters, else set the only parameter to `'args'`. Args will contain a list of whatever arguments were passed to the command.

This command will contain whatever logic needs to be carried out. You should validate the arguments in there. After you have the response that you want a user to see, just 'return' it.

Let's say we want to add a command which will take two arguments, we will call it `'!random'` and it will take a `'minimum'` and `'maximum'` argument. We will limit this command to be allowed to be called every 20 seconds.

Add the following to the `'commands'` dictionary in `src/lib/command_headers.py`:

```python
'!random': {
    'limit': 20,
    'argc': 2,
    'return': 'command',
    'ul': 'mod',
    'space_case': True
}
```

`'limit'` refers to the cooldown. The cooldown is only active per separate channel

`'argc'` refers to the number of arguments a command accepts, separated by spaces. If the command does not have `'command'` as its `'return'` value, this is not necessary. However, even if there are no arguments and `'command'` is listed, `0` should be used.

If a command is not intended for use by moderators, there is no need for `'ul'` to be included

a `'space_case'` is a special scenario where you would like a command to have a single argument, but no limits to the number of separate strings you can input. Normally, arguments are separated by spaces.

### Whispers
If a user tries to type a message that is currently on a cooldown, the bot will whisper the user directly. It will inform them that they need to chill and how much more time they have until they can use it again. It will also let them know that they can just try to use the command in the whisper message itself. Users can type whatever they want to the bot and it will reply with quite a few responses defined in the `brain` directory using a language called `RiveScript` [https://www.rivescript.com/](https://www.rivescript.com/) . There is also an API for quotes that the bot hits when it gets stumped so it sounds smart. The API is provided by [http://forismatic.com/en/api/](http://forismatic.com/en/api/) . The bot can be whispered by typing

```
/w Jadebot hi
```

into any chatroom on Twitch.
