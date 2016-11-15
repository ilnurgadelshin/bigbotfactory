# -*- coding: utf-8 -*-

from bots.dfa_modules.admin_tools_module import AdminToolsModule
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands
from bots.generic_dfas.bot_stats_dfa import BotStatsDFA

from bots.bbfbot.tutorials import BROADCAST_ADMIN_TUTORIAL
from bots.broadcast_bot_handler.custom_commands_module import CustomCommandViewDFA, CustomCommandOutputDFA
from bots.broadcast_bot_handler.new_post_module import NewPostDFA


class BroadcastBotStartDFA(TelegramDFADefinedCommands):
    ADMIN_TOOLS = 'Admin tools'
    NEW_POST = 'New Post'
    CUSTOM_MENU = 'Custom Menu'
    STATS = 'Stats'


    def _intern_dump(self, existing_ids):
        return {}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
        )

    def update_menu(self, update):
        if self.bot_handler.is_admin():
            self.set_command(
                self.STATS,
                BotStatsDFA(self.chat_id, self.bot_handler, self), self.bot_handler.is_admin())
            self.set_command(self.NEW_POST, NewPostDFA(self.chat_id, self.bot_handler, self))
            self.set_command(self.CUSTOM_MENU, CustomCommandViewDFA(self.chat_id, self.bot_handler, None))
            self.set_command(self.ADMIN_TOOLS, AdminToolsModule(self.chat_id, self.bot_handler, self, BROADCAST_ADMIN_TUTORIAL))
        keyboard = CustomCommandOutputDFA.upgrade_defined_dfa(self, None)
        if self.bot_handler.is_admin():
            keyboard.append([self.NEW_POST, self.CUSTOM_MENU])
            keyboard.append([self.ADMIN_TOOLS, self.STATS])
        self.set_keyboard(keyboard)
