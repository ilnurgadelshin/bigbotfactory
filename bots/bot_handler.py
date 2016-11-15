# -*- coding: utf-8 -*-

import re
import logging
import random
import string

from bots.bot_command import TelegramBotCommand
from bots.utils.bot_handler_utils import BotHandlerUtils
from telegram.objects.update import TelegramUpdate
from telegram.objects.message import TelegramMessage
from telegram.objects.user import TelegramUser
from aws_telegram.aws_api_handler import TelegramAWSAPIHandler
from bots.libs.entities.bot_admins import BotAdmins
from bots.libs.entities.bot_info import BotInfo
from bots.libs.entities.bot_user_state import BotUserState
from bots.libs.entities.bot_state import BotState

logger = logging.getLogger(__name__)


class BotHandler(object):
    ONE_TIME_CODE_PREFIX = 'bigadmin_'

    def __init__(self, token, update):
        self.api_handler = TelegramAWSAPIHandler(token)
        assert isinstance(update, TelegramUpdate)
        self.update = update
        self.bot_id = self.api_handler.get_bot_id()
        self.chat_id = self.update.message.chat.id

        # self.user_context = UserState(self.chat_id)
        self.bot_user_context = BotUserState(self.bot_id, self.chat_id)

        self.bot_user = None

        self.send_output_messages_async = False
        self.output_messages = []
        self.output_reply = None
        self._is_admin = None

    @staticmethod
    def is_hashed_properly(text):
        sum = 0
        for s in text:
            sum += ord(s) - ord('a')
        return sum % 100 == 0

    def generate_one_time_code(self):
        one_time_admins_code = ""
        while True:
            one_time_admins_code = ''.join(random.choice(string.ascii_letters) for _ in range(45))
            if self.is_hashed_properly(one_time_admins_code):
                break
        one_time_admins_code = BotHandler.ONE_TIME_CODE_PREFIX + one_time_admins_code
        BotState(self.bot_id).set_value('one_time_admins_code', one_time_admins_code)
        return one_time_admins_code

    def get_one_time_code(self):
        code = BotState(self.bot_id).get_value('one_time_admins_code')
        if code is None:
            code = self.generate_one_time_code()
        return code

    def maybe_one_time_code(self, text):
        return text.startswith(BotHandler.ONE_TIME_CODE_PREFIX) and \
              self.is_hashed_properly(text[len(BotHandler.ONE_TIME_CODE_PREFIX):])

    def is_one_time_code(self, text):
        if text.startswith("/start "):
            text = text[len("/start "):]
        if not self.maybe_one_time_code(text):
            return False
        return self.get_one_time_code() == text

    def get_me(self):
        if self.bot_user is None:
            self.bot_user = self.api_handler.get_me()
            assert isinstance(self.bot_user, TelegramUser)
        return self.bot_user

    def set_about(self, new_about):
        if not new_about:
            return False
        BotInfo(self.api_handler.get_bot_id()).set_about(new_about)
        return True

    def show_about(self):
        about = BotInfo(self.bot_id).get_about()
        if about is not None:
            self.api_handler.send_message(self.update.message.chat.id, text=about)
        footer = BotHandlerUtils.get_rate_us_message(self.get_me())
        footer += BotHandlerUtils.get_contact_us_message()
        self.api_handler.send_message(self.update.message.chat.id, text=footer, disable_web_page_preview=True)

    @TelegramBotCommand('ping', admin_only=True, short_description='should respond with pong')
    def _ping(self):
        self.add_output_text('pong')

    @TelegramBotCommand('get_admins', admin_only=True, short_description='a list of admin ids')
    def _get_admins(self):
        admins_text = "Admin ids: " + ", ".join(map(str, self.get_admins().keys()))
        self.add_output_text(admins_text)

    @TelegramBotCommand('remove_admin', admin_only=True, short_description='remove an admin')
    def _remove_admin(self):
        self.remove_admin(int(self.update.message.text))
        self.add_output_text('admin has been removed. see /get_admins')

    @TelegramBotCommand('help', short_description='list all available commands')
    def _list(self):
        output = []
        for header, is_admin in {'Admin Commands:': True, 'Available commands:': False}.iteritems():
            sub_output = ""
            for cmd, func in self._get_all_bot_commands().iteritems():
                if func.admin_only != is_admin:
                    continue
                str = '\n/' + cmd
                if func.short_description is not None:
                    str += ' - ' + func.short_description
                sub_output += str
            if sub_output:
                output.append(header + sub_output)

        if not len(output):
            output = ["No available commands"]
        self.add_output_text(text="\n\n".join(output))

    def _get_all_bot_commands(self, should_match_text=None):
        result = {}
        for field_name in dir(self):
            field = self.__getattribute__(field_name)
            if hasattr(field, 'telegram_bot_command'):
                telegram_bot_command = field.telegram_bot_command
                if should_match_text is not None and not should_match_text.startswith(u'/' + telegram_bot_command):
                    # no way this command matches the given text
                    continue
                if hasattr(field, 'admin_only') and field.admin_only and not self.is_admin():
                    continue
                result[telegram_bot_command] = field
        return result

    def is_admin(self):
        if self._is_admin is None:
            self._is_admin = BotAdmins(self.bot_id).is_admin(self.chat_id)
        return self._is_admin

    def get_admins(self):
        return BotAdmins(self.bot_id).get_all_admins()

    def get_admins_count(self):
        return BotAdmins(self.bot_id).get_admins_count()

    def add_admin(self, user):
        if self.get_admins_count() < 10:  # it's better to restrict the number of admins instead of allowing any number
            BotAdmins(self.api_handler.get_bot_id()).add_admin(user)

    def remove_admin(self, user_id):
        BotAdmins(self.api_handler.get_bot_id()).remove_admin(user_id)

    def process_on_given_token(self):
        return False

    def add_output_message(self, message):
        assert isinstance(message, TelegramMessage)
        self.output_messages.append(message)

    def add_output_text(self, text):
        self.add_output_message(TelegramMessage.gen_fake_text_message(0, text))

    def set_output_reply(self, reply):
        self.output_reply = reply

    def process(self):
        text = self.update.message.text
        # we explicitly remove all bots' names occurrences to have this bot work in chats
        if self.chat_id < 0 and text is not None:
            self.update.message.text = re.sub(r'@[\w]+', '', text)

        # this is a secret feature. If the user submits this bot's token or one time code, then we add him/her to admins
        if (text is not None) and (self.chat_id > 0) and \
                (self.api_handler.is_token(text) or self.is_one_time_code(text)):
            self.add_admin(self.update.message.from_)
            self.generate_one_time_code()
            self.api_handler.send_message(self.chat_id, text="You've been successfully added as an admin")
            if not self.process_on_given_token():
                return

        stop_after = False
        if (text is not None) and (text.startswith('/')):
            for cmd, function in self._get_all_bot_commands(text).iteritems():
                cmd_prefix = u'/' + cmd
                if text.startswith(cmd_prefix):
                    self.update.message.text = self.update.message.text[len(cmd_prefix):].strip()
                    function()
                    stop_after = True
                    if hasattr(function, 'stop_after'):
                        stop_after = bool(getattr(function, 'stop_after'))
                    break
        if not stop_after:
            self._process()

        # output all gathered messages
        if self.output_reply is not None and len(self.output_messages) == 0:
            self.add_output_text(u'\u00a0')
        if len(self.output_messages):
            self.api_handler.send_telegram_messages(
                [self.chat_id], messages=self.output_messages,
                reply_markup=self.output_reply, async=self.send_output_messages_async)

    def _process(self):
        raise NotImplementedError
