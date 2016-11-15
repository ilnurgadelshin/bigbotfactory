# -*- coding: utf-8 -*-

from bots.telegram_dfa import TelegramDFA
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands
from bots.generic_dfas.simple_reply import TelegramDFASimpleReply
from bots.generic_dfas.about_dfa import TelegramDFAAbout
from bots.generic_dfas.confirmation_dfa import TelegramDFAConfirm
from bots.bbfbot.tutorials import SEND_A_TOKEN_TUTORIAL, BROADCAST_ADMIN_TUTORIAL

from telegram.api.core.api import TelegramAPIHandler
from telegram.objects.user import TelegramUser
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot

from bots.libs.entities.bot_admins import BotAdmins
from bots.libs.entities.bot_owners import OwnedBots
import re
from bots.bots_factory import BotsFactory


class TelegramDFAEnterToken(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'
    TUTORIAL = 'Tutorial'

    TOKEN_REGEXP = re.compile(r'\d+:[a-zA-Z0-9_\-]{35}')

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler,
                                            default_message='Please forward me the message from @BotFather containing '
                                                            'the API token, or just enter it below')
        self.exit_dfa = exit_dfa
        self.set_command(self.CANCEL, exit_dfa)
        self.set_command(self.TUTORIAL, TelegramDFASimpleReply(chat_id, bot_handler, SEND_A_TOKEN_TUTORIAL, self))
        self.set_keyboard([[self.TUTORIAL, self.CANCEL]])

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def get_token_from_text(self, text):
        s = re.findall(self.TOKEN_REGEXP, text)
        if len(s):
            return s[0]
        return None

    def add_bot(self, token, bot_user, chat_admin):
        assert chat_admin.id == self.chat_id
        owner_id = OwnedBots.get_owner_for_bot(bot_user.id)
        if owner_id is not None:
            if owner_id != self.chat_id:
                self.add_output_text(text='This token is already owned. The owner has been notified')
                api_handler = TelegramAPIHandler(token)
                api_handler.send_message(owner_id, text="Someone is trying to hijack this bot. Look out!")
            else:
                self.add_output_text(text='This token is already in use')
            return

        owner = OwnedBots(self.chat_id)
        owner.add_bot(bot_user, token)
        self.add_output_text(text='Thanks! A new token was added: @' + bot_user.username)
        BBFAlarmBot.alarm_developers("New bot: @" + bot_user.username)

        new_bot_api_handler = TelegramAPIHandler(token)
        new_bot_api_handler.set_webhook(
            self.bot_handler.web_hook + "/" + BotsFactory.BROADCAST_BOT + "/" + token + "/" + bot_user.username)
        BotAdmins(bot_user.id).add_admin(chat_admin, async=False)  # async is False, otherwise admins won't be admins
        return self.exit_dfa

    def process_input(self, update):
        text = update.message.text
        if text:
            token = self.get_token_from_text(text)
            if token is None:
                self.add_output_text(text="Sorry but we couldn't find a token in your text. Please try again")
                return
            try:
                bot_user = TelegramAPIHandler(token).get_me()
            except:
                bot_user = None
            if bot_user is None:
                self.add_output_text(text='Invalid token. Please try again.')
                return
            owner = OwnedBots(self.chat_id)
            if owner.get_bots_count() >= 20:
                self.add_output_text(text='Sorry, you cannot add more than 20 bots')
                return self.exit_dfa
            return self.add_bot(token, bot_user, update.message.from_)


class TelegramDFADeleteBot(TelegramDFA):
    def __init__(self, chat_id, bot_handler, bot_id, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.bot_id = bot_id
        self.exit_dfa = exit_dfa

    def on_terminate(self, update):
        self.add_output_text(text="We are sorry to hear that you've decided to delete your bot.")
        owner = OwnedBots(self.chat_id)
        bot = owner.get_bot(self.bot_id)
        TelegramAPIHandler(bot['token']).set_webhook('')
        owner.remove_bot(self.bot_id)
        BBFAlarmBot.alarm_developers("Bot deleted: @" + TelegramUser.gen_from_json_str(bot['bot_user_str']).username)
        return self.exit_dfa

    def _intern_dump(self, existing_ids):
        return {'bot_id': self.bot_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['bot_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )


class TelegramDFAViewBot(TelegramDFADefinedCommands):
    DELETE = 'Delete'
    BACK = 'Back'

    def __init__(self, chat_id, bot_handler, bot_id, bot_name, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa
        self.bot_id = bot_id
        self.bot_name = bot_name

    def _intern_dump(self, existing_ids):
        return {'bot_id': self.bot_id, 'bot_name': self.bot_name, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['bot_id'],
            dumped_object['bot_name'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        message = 'You can make further edits and create posts directly in your bot: @' + self.bot_name + \
                  " or click https://telegram.me/" + self.bot_name + "?start=start"
        self.set_message(message)
        self.set_command(self.DELETE, TelegramDFAConfirm(
            self.chat_id, self.bot_handler,
            default_text="Are you sure you want to delete?",
            confirm_dfa=TelegramDFADeleteBot(self.chat_id, self.bot_handler, self.bot_id, self.exit_dfa),
            no_dfa=self))
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.DELETE, self.BACK]])


class TelegramDFATutorial(TelegramDFADefinedCommands):
    BACK = 'Back'
    TOKEN_TUTORIAL = 'How to create a bot'
    BROADCAST_ADMIN_TUTORIAL = 'How to manage your bot'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message='Select a bot')
        self.exit_dfa = exit_dfa
        self.set_command(self.TOKEN_TUTORIAL, TelegramDFASimpleReply(chat_id, bot_handler, SEND_A_TOKEN_TUTORIAL, self))
        self.set_command(self.BROADCAST_ADMIN_TUTORIAL,
                         TelegramDFASimpleReply(chat_id, bot_handler, BROADCAST_ADMIN_TUTORIAL, self))
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.TOKEN_TUTORIAL], [self.BROADCAST_ADMIN_TUTORIAL], [self.BACK]])
        self.set_message('Thanks for using BBF!')

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )


class TelegramDFAMyBots(TelegramDFADefinedCommands):
    BACK = 'Back'
    CREATE_BOT = 'Create a bot'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message='Select a bot')
        self.exit_dfa = exit_dfa
        self.set_command(self.CREATE_BOT, TelegramDFAEnterToken(self.chat_id, self.bot_handler, exit_dfa))
        self.set_command(self.BACK, self.exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        for cmd in self.get_command_names():
            if cmd != self.BACK and cmd != self.CREATE_BOT:
                self.set_enable(cmd, False)
        keyboard = []
        owner = OwnedBots(self.chat_id)

        for bot_id, bot_info in owner.get_all_owned_bots().iteritems():
            bot_user = TelegramUser.gen_from_json_str(bot_info['bot_user_str'])
            bot_name = bot_user.username
            if self.has_command(bot_name):
                self.set_enable(bot_name, True)
            else:
                self.set_command(bot_name, TelegramDFAViewBot(self.chat_id, self.bot_handler, bot_id, bot_name, self))
            keyboard.append([bot_name])
        keyboard.append([self.CREATE_BOT])
        keyboard.append([self.BACK])
        self.set_keyboard(keyboard)


class BBFDFA(TelegramDFADefinedCommands):
    CREATE_BOT = 'Create a bot'
    MY_BOTS = 'My bots'
    ABOUT = 'About'
    TUTORIAL = 'Tutorial'

    def __init__(self, chat_id, bot_handler):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message='Select a command')
        commands = {
            self.TUTORIAL: (TelegramDFATutorial(chat_id, bot_handler, self), None),
            self.CREATE_BOT: (TelegramDFAEnterToken(chat_id, bot_handler, self), None),
            self.ABOUT: (TelegramDFAAbout(chat_id, bot_handler, self), None),
            self.MY_BOTS: (TelegramDFAMyBots(chat_id, bot_handler, self), 'List all my bots'),
        }
        for cmd, cmd_description in commands.iteritems():
            self.set_command(cmd, cmd_description[0], short_description=cmd_description[1])
        keyboard = [[self.CREATE_BOT, self.MY_BOTS], [self.TUTORIAL, self.ABOUT]]
        self.set_keyboard(keyboard)

    def _intern_dump(self, existing_ids):
        return {}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
        )
