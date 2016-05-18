"""
Intricate Chat Bot for Twitch.tv with Whispers

By Shane Engelman <me@5h4n3.com>

Contributions from dustinbcox and theepicsnail
"""

import sys
from threading import Thread

import lib.functions_commands as commands
import src.lib.command_headers
import src.lib.cron as cron
import src.lib.rive as rive
from lib.functions_general import pbot
from src.config.config import config
from src.lib.irc import IRC
from src.lib.points import modify_points
from src.models.model import Channel, Message, User, Command
from src.lib.twitch import Twitch
from src.lib.moderators import get_moderator

reload(sys)
sys.setdefaultencoding("utf8")

PRIMARY_CHANNEL = config["channels"][0].lstrip("#")
BOT_USER = config["username"].lstrip("#")
SUPERUSER = config["superuser"].lstrip("#")
TEST_USER = config["test_user"].lstrip("#")
EXTRA_CHANNEL = "lorenzotherobot".lstrip("#")

NICKNAME = config["username"].lstrip("#")
PASSWORD = config["oauth_password"]


class Bot(object):

    def __init__(self):
        self.IRC = IRC(config)
        self.nickname = NICKNAME
        self.password = PASSWORD
        self.config = config
        self.crons = self.config.get("cron", {})
        cron.initialize(self.IRC, self.crons)
        src.lib.command_headers.initalizeCommands(config)
        self.run()

    def return_custom_command(self, chan, trigger, username):
        Channel.get_or_create(channel=chan)
        try:
            command = Command.get(
                trigger=trigger,
                channel=Channel.get(channel=chan).id)
            Command.update(times_used=Command.times_used+1).where(
                Command.trigger == trigger,
                Command.channel == Channel.get(channel=chan).id
            ).execute()
            resp = command.response
            return resp
        except Command.DoesNotExist:
            return

    def privmsg(self, username, channel, message):
        if (channel == "#" + PRIMARY_CHANNEL or
                channel == "#" + SUPERUSER or
                channel == "#" + TEST_USER):
            if username == "twitchnotify":
                self.check_for_sub(channel, [username], message)
            # TODO add spam detector here
        chan = channel.lstrip("#")
        if message[0] == "!":
            trigger = message.split()[0]
            fetch_command = self.return_custom_command(
                chan, trigger.lstrip("!"), username)
            if fetch_command:
                self.IRC.send_message(channel, fetch_command)
        # self.save_message(username, channel, message)
        part = message.split(' ')[0]
        valid = False
        if commands.is_valid_command(message):
            valid = True
        if commands.is_valid_command(part):
            valid = True
        if not valid:
            return
        resp = self.handle_command(
            part, channel, username, message)
        if resp:
            self.IRC.send_message(channel, resp)
        return

    def whisper(self, username, channel, message):
        message = str(message.lstrip("!"))
        resp = rive.Conversation(self).run(username, message)[:350]
        # self.save_message(username, "WHISPER", message)
        if resp:
            print "!->", resp
            # self.save_message(BOT_USER, "WHISPER", resp)
            self.IRC.send_whisper(username, str(resp))
            return

    def handle_command(self, command, channel, username, message):
        User.get_or_create(username=username)
        moderator = get_moderator(channel, username)
        if command == message:
            args = []
        elif command == message and command in commands.keys():  # pragma: no cover
            pass
        else:
            args = [message[len(command) + 1:]]
        if not commands.check_is_space_case(command) and args:
            args = args[0].split(" ")
        if commands.is_on_cooldown(command, channel) and not moderator:
            pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                command, username, commands.get_cooldown_remaining(
                    command, channel)), channel)
            self.IRC.send_whisper(
                username, "Sorry! " + command +
                " is on cooldown for " + str(
                    commands.get_cooldown_remaining(
                        command, channel)
                ) + " more seconds in " + channel.lstrip("#") +
                ". Can I help you?")
            return
        if commands.check_has_user_cooldown(command) and not moderator:
            if commands.is_on_user_cooldown(command, channel, username):
                self.IRC.send_whisper(
                    username, "Slow down! Try " + command +
                    " in " + channel.lstrip("#") + " in another " + str(
                        commands.get_user_cooldown_remaining(
                            command, channel, username)) + " seconds or just \
ask me directly?")
                return
            commands.update_user_last_used(command, channel, username)
        pbot('Command is valid and not on cooldown. (%s) (%s)' %
             (command, username), channel)
        cmd_return = commands.get_return(command)
        if cmd_return != "command":
            resp = '(%s) : %s' % (username, cmd_return)
            commands.update_last_used(command, channel)
            self.IRC.send_message(channel, resp)
            return
        if commands.check_has_user_level(username, command):
            if not moderator and username != SUPERUSER:
                if commands.commands[command].get("optional") is not None and len(
                        message.split(" ")) < 2:
                    pass
                else:
                    resp = '(%s) : %s' % (
                        username, "This is a moderator-only command!")
                    pbot(resp, channel)
                    self.IRC.send_whisper(username, resp)
                    return
        approved_channels = [
            PRIMARY_CHANNEL, BOT_USER, SUPERUSER, TEST_USER, EXTRA_CHANNEL]
        if channel.lstrip("#") not in approved_channels:
            prevented_list = []
            if command.lstrip("!") in prevented_list:
                return
        result = commands.pass_to_function(
            command, args, username=username, channel=channel.lstrip("#"),
            irc=self.IRC)
        commands.update_last_used(command, channel)
        if result:
            resp = '(%s) : %s' % (username, result)
            pbot(resp, channel)
            # self.save_message(BOT_USER, channel, resp)  # pragma: no cover
            return resp[:350]

    def check_for_sub(self, channel, username, message):
        try:
            message_split = message.rstrip("!").split()
            subbed_user = message_split[0]
            if message_split[1] == "just" and len(message_split) < 4:
                modify_points(channel.lstrip("#"), [subbed_user], "add", 100)
                resp = "/me {0} ammo for {1} for a first \
time subscription!".format(100, subbed_user)
                self.IRC.send_message(channel, resp)
                # self.save_message(BOT_USER, channel, resp)
            elif message_split[1] == "subscribed" and len(message_split) < 9:
                months_subbed = message_split[3]
                modify_points(
                    channel.lstrip("#"), [subbed_user], "add", int(months_subbed) * 100)
                resp = "/me {0} has just resubscribed for {1} \
months straight and is getting {2} ammo for loyalty!".format(
                    subbed_user, months_subbed, int(months_subbed) * 100)
                self.IRC.send_message(channel, resp)
                # self.save_message(BOT_USER, channel, resp)
        except Exception as error:  # pragma: no cover
            print error

    def save_message(self, username, channel, message):
        channel = channel.lstrip("#")
        User.get_or_create(username=username)
        Channel.get_or_create(channel=channel)
        username_id = User.get(username=username).id
        channel_id = Channel.get(channel=channel).id
        Message.create(
            username=username_id, channel=channel_id, message=message)

    def run(self):

        def get_incoming_data(kind):
            while True:
                try:
                    data = self.IRC.nextMessage(kind)
                    if kind == "chat":
                        message = self.IRC.check_for_message(data)
                    if kind == "whisper":
                        message = self.IRC.check_for_whisper(data)
                    if not message:
                        continue
                    if message:
                        if kind == "chat":
                            data = self.IRC.get_message(data)
                        if kind == "whisper":
                            data = self.IRC.get_whisper(data)
                        message_dict = data
                        channel = message_dict.get('channel')
                        message = message_dict.get('message')
                        username = message_dict.get('username')
                        print "->*", username, channel, message
                        if message and kind == "chat":
                            Thread(target=self.privmsg, args=(
                                username, channel, message)).start()
                        if message and kind == "whisper":
                            Thread(target=self.whisper, args=(
                                username, channel, message)).start()
                    continue
                except Exception as error:
                    print error

        Thread(target=get_incoming_data, args=("whisper",)).start()
        Thread(target=get_incoming_data, args=("chat",)).start()
