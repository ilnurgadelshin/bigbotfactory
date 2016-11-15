# -*- coding: utf-8 -*-

from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands
from bots.dfa_modules.admins import AdminsModule
from bots.dfa_modules.channels_module import ChannelsModule
from bots.generic_dfas.simple_reply import TelegramDFASimpleReply

from bots.generic_dfas.about_dfa import TelegramDFASetAbout


PUBLISH_ON_STOREBOT_TUTORIAL = """
Due to some circumstances we are not able to provide you with an automatic way of publishing your bot on Store,

You have to follow next steps:

1. Login to Store: https://storebot.me/login
2. Add your bot's description on this page: https://storebot.me/add
3. Wait for approval
4. Start growing your audience

We are still in touch with storebot and working on building a better service for you.
"""


class AdminToolsModule(TelegramDFADefinedCommands):
    BACK = u'⬅️'
    ADMIN_TOOLS = 'Admins'
    CHANNELS_MODULE = 'Manage Channels'
    STOREBOT_PUBLISHER = 'Publish on Store'
    SET_ABOUT = 'Set About'

    HELP = 'Help'

    def __init__(self, chat_id, bot_handler, exit_dfa, help_text=None):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Admin tools')
        self.exit_dfa = exit_dfa
        self.help_text = help_text


    def _intern_dump(self, existing_ids):
        return {'help_text': self.help_text,
                'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context),
            dumped_object['help_text'],
        )

    def update_menu(self, update):
        keyboard = []
        if self.bot_handler.is_admin():
            self.set_command(self.ADMIN_TOOLS, AdminsModule(self.chat_id, self.bot_handler, self))
            self.set_command(self.STOREBOT_PUBLISHER,
                             TelegramDFASimpleReply(self.chat_id, self.bot_handler, PUBLISH_ON_STOREBOT_TUTORIAL, self))
            self.set_command(self.SET_ABOUT, TelegramDFASetAbout(self.chat_id, self.bot_handler, self))
            self.set_command(self.CHANNELS_MODULE, ChannelsModule(self.chat_id, self.bot_handler, self))
            keyboard.append([self.ADMIN_TOOLS])
            keyboard.append([self.CHANNELS_MODULE])
            keyboard.append([self.STOREBOT_PUBLISHER])
            keyboard.append([self.SET_ABOUT])
        if self.help_text:
            self.set_command(self.HELP, TelegramDFASimpleReply(self.chat_id, self.bot_handler, self.help_text, self))
            keyboard.append([self.HELP])
        self.set_command(self.BACK, self.exit_dfa)
        keyboard.append([self.BACK])
        self.set_keyboard(keyboard)
