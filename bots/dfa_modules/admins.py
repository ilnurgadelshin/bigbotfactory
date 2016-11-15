# -*- coding: utf-8 -*-

from bots.telegram_dfa import TelegramDFA, TelegramDFAGoToInitialDFAException
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands


class DeleteAdminDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, admin_id, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa
        self.admin_id = admin_id

    def _intern_dump(self, existing_ids):
        return {'admin_id': self.admin_id,
                'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['admin_id'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        self.bot_handler.remove_admin(self.admin_id)
        if self.chat_id == self.admin_id:
            self.add_output_text("You've been removed from admins. Please, send a new message")
            raise TelegramDFAGoToInitialDFAException
        return self.exit_dfa


class AdminViewDFA(TelegramDFADefinedCommands):
    REMOVE = 'Remove'
    BACK = u'⬅️'

    def __init__(self, chat_id, bot_handler, admin_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.admin_id = admin_id
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'admin_id': self.admin_id,
                'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['admin_id'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def update_menu(self, update):
        text = "Admin: " + str(self.admin_id)
        self.set_message(text)
        self.set_command(self.REMOVE, DeleteAdminDFA(self.chat_id, self.bot_handler, self.admin_id, self.exit_dfa))
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.REMOVE, self.BACK]])


class ViewOneTimeCodeDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        text = "If you want to add a new admin, send this link: https://telegram.me/" + \
               self.bot_handler.get_me().username + "?start=" + self.bot_handler.get_one_time_code() + \
               " \nor let him send/forward this code to the bot:"
        self.add_output_text(text)
        self.add_output_text(self.bot_handler.get_one_time_code())
        return self.exit_dfa


class AdminsModule(TelegramDFADefinedCommands):
    ADMINS = 'Admins'
    BACK_BUTTON = 'Back'
    ONE_TIME_CODE = 'Add an admin'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Admins')
        self.exit_dfa = exit_dfa
        self.set_command(self.ONE_TIME_CODE, ViewOneTimeCodeDFA(self.chat_id, self.bot_handler, self))
        self.set_command(self.BACK_BUTTON, self.exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def update_menu(self, update):
        if update.message.chat.id < 0:
            self.add_output_text("Admin Tool is not available for chats")
            return self.exit_dfa

        for command in self.get_command_names():
            if isinstance(self.get_command_dfa(command), AdminViewDFA):
                self.set_enable(command, False)

        keyboard = []
        for admin in self.bot_handler.get_admins().values():
            command = admin.first_name
            if admin.last_name is not None:
                command += " " + admin.last_name
            if admin.username is not None:
                command += " (" + admin.username + ")"
            if not self.has_command(command):
                self.set_command(command, AdminViewDFA(self.chat_id, self.bot_handler, admin.id, self))
            else:
                self.set_enable(command, True)
            keyboard.append([command])
        keyboard.append([self.ONE_TIME_CODE])
        keyboard.append([self.BACK_BUTTON])
        self.set_keyboard(keyboard)
