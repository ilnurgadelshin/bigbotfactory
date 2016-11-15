# -*- coding: utf-8 -*-

from bots.dfa_bot_handler import DFABotHandler
from bots.bot_command import TelegramBotCommand
from bots.broadcast_bot_handler.broadcast_bot_dfa import BroadcastBotStartDFA
from bots.broadcast_bot_handler.custom_command_type import CustomCommandType
from telegram.objects.message import TelegramMessage

from bots.libs.entities.bot_info import BotInfo
from bots.libs.entities.bot_subscribers import BotSubscribers
from bots.libs.entities.bot_channels import BotChannels
from bots.libs.entities.bot_custom_commands import BotCustomCommands

import random
import time


class BroadcastBotHandler(DFABotHandler):
    def __init__(self, token, update):
        DFABotHandler.__init__(self, token, update)
        self.send_output_messages_async = False

    def _initial_dfa(self):
        return BroadcastBotStartDFA(self.chat_id, self)

    def _on_first_time_visit(self):
        subscription = BotSubscribers(self.api_handler.get_bot_id()).get_subscription(self.chat_id)
        if subscription is None:
            self.subscribe(self.chat_id)

    def process_on_given_token(self):
        return True

    def create_command(self, name, parent_id=None):
        assert isinstance(name, basestring)
        cmd_id = None
        while cmd_id is None:
            cmd_id = random.randint(1001, 10000000)
            if self.has_command(cmd_id):
                cmd_id = None
        BotCustomCommands(self.api_handler.get_bot_id()).save_command(
            cmd_id, parent_id, name, [], CustomCommandType.ALL_MESSAGES, None, None)
        return cmd_id

    def find_children(self, parent_id=None):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_child_commands(parent_id)

    def remove_command(self, cmd_id, is_root=True):
        # we should async-ly remove all child commands as well.
        BotCustomCommands(self.api_handler.get_bot_id()).remove_commands([cmd_id])

    def set_command_name(self, cmd_id, name):
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_name(cmd_id, name)

    def get_command(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command(cmd_id)

    def is_root(self, cmd_id):
        return cmd_id is None or cmd_id == BotCustomCommands.NO_PARENT_ID

    def get_command_name(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command(cmd_id).get('command_name')

    def set_command_xy(self, cmd_id, x=None, y=None):
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_xy(cmd_id, x, y)

    def get_command_xy(self, cmd_id):
        command = BotCustomCommands(self.api_handler.get_bot_id()).get_command(cmd_id)
        return command.get('x'), command.get('y')

    def get_command_names(self, parent_id=None):
        commands = BotCustomCommands(self.api_handler.get_bot_id()).get_child_commands(parent_id)
        result = {}
        for cmd_id, command in commands.iteritems():
            result[cmd_id] = command['command_name']
        return result

    def set_command_type(self, cmd_id, cmd_type):
        assert cmd_type in [CustomCommandType.ALL_MESSAGES, CustomCommandType.RANDOM_MESSAGE]
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_type(cmd_id, cmd_type)

    def get_command_type(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command(cmd_id).get('cmd_type')

    def add_message(self, cmd_id, message):
        messages = BotCustomCommands(self.api_handler.get_bot_id()).get_command_messages(cmd_id)
        assert isinstance(message, TelegramMessage)
        messages.append(message)
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_messages(cmd_id, messages)

    def set_message(self, cmd_id, index, message):
        messages = BotCustomCommands(self.api_handler.get_bot_id()).get_command_messages(cmd_id)
        assert isinstance(message, TelegramMessage)
        if 0 <= index < len(messages):
            messages[index] = message
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_messages(cmd_id, messages)

    def remove_message(self, cmd_id, index):
        messages = BotCustomCommands(self.api_handler.get_bot_id()).get_command_messages(cmd_id)
        if 0 <= index < len(messages):
            messages.pop(index)
        BotCustomCommands(self.api_handler.get_bot_id()).set_command_messages(cmd_id, messages)

    def get_message(self, cmd_id, index):
        if not self.has_command(cmd_id):
            return
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command_message(cmd_id, index)

    def get_command_messages(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command_messages(cmd_id)

    def get_command_messages_count(self, cmd_id):
        return len(self.get_command_messages(cmd_id))

    def has_command(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).has_command(cmd_id)

    def get_command_parent(self, cmd_id):
        return BotCustomCommands(self.api_handler.get_bot_id()).get_command_parent(cmd_id)

    def get_command_path(self, cmd_id):
        if self.is_root(cmd_id):
            return "root"
        return self.get_command_name(cmd_id)


    def get_channels(self):
        return BotChannels(self.api_handler.get_bot_id()).get_all_channels()

    def has_channel(self, channel_name):
        return BotChannels(self.api_handler.get_bot_id()).has_channel(channel_name)

    def add_channel(self, channel_name):
        BotChannels(self.api_handler.get_bot_id()).add_channel(channel_name)

    def remove_channel(self, channel_name):
        BotChannels(self.api_handler.get_bot_id()).remove_channel(channel_name)

    def subscribe(self, chat_id):
        self._show_about()
        BotSubscribers(self.api_handler.get_bot_id()).subscribe(chat_id)

    @TelegramBotCommand('on', short_description='subscribe', stop_after=False)
    def _on_subscription(self):
        self.subscribe(self.chat_id)

    @TelegramBotCommand('off', short_description='unsubscribe', stop_after=False)
    def _off_subscription(self):
        BotSubscribers(self.api_handler.get_bot_id()).unsubscribe(self.chat_id)
        self.add_output_text("You are unsubscribed from this bot. Use /on to subscribe."
                             "\nCreate your own bot: @bbfbot")

    @TelegramBotCommand('about', short_description='show about')
    def _show_about(self):
        about = BotInfo(self.bot_id).get_about()
        if about is None:
            about = ""
        about += """
         Use /on and /off to manage your subscription. /help to see default commands.
         Create your own bot: @bbfbot
        """
        self.add_output_text(about)


if __name__ == '__main__':
    from telegram.objects.update import TelegramUpdate
    from telegram.api.core.api import TelegramAPIHandler
    from bots.libs.entities.bot_user_state import BotUserState
    import datetime

    chat_id = 123456789
    token = '212875847:AAGwZ7J2mcRttwmLjgc5PWsnT2zZIYIsSaw'
    debug_api_handler = TelegramAPIHandler(token)
    bot_user_state = BotUserState(debug_api_handler.get_bot_id(), chat_id)
    bot_user_state.clear_state()

    messages = [
        u'⬅️',
    ]
    debug_api_handler.send_message(chat_id, 'Starting a new test: ' + str(datetime.datetime.now()))
    for m in messages:
        debug_api_handler.send_message(chat_id, 'Received a message:\n' + m)
        update = TelegramUpdate(chat_id, TelegramMessage.gen_fake_text_message(chat_id, m))
        handler = BroadcastBotHandler(token, update)
        handler.process()
        time.sleep(1)
