# -*- coding: utf-8 -*-

from bots.telegram_dfa import TelegramDFA
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands
from bots.broadcast_bot_handler.custom_command_type import CustomCommandType


class SetCustomCommandType(TelegramDFA):
    def __init__(self, chat_id, bot_handler, cmd_id, cmd_type, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.cmd_type = cmd_type
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'cmd_type': self.cmd_type, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['cmd_type'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        self.bot_handler.set_command_type(self.cmd_id, self.cmd_type)
        return self.exit_dfa


class AddMessageToCommandDFA(TelegramDFADefinedCommands):
    DONE = 'Done'

    def __init__(self, chat_id, bot_handler, cmd_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.set_command(self.DONE, exit_dfa)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        count = self.bot_handler.get_command_messages_count(self.cmd_id)
        if count > 20:
            self.add_output_text(text="Sorry but no more messages are allowed")
            return self.exit_dfa
        self.set_message('Enter a new message or hit "Done"')

    def process_input(self, update):
        message = update.message
        if message.has_non_empty_content():
            self.bot_handler.add_message(self.cmd_id, message)


class ViewCommandsMessageOutputDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, cmd_id, index, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.index = index
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'index': self.index, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['index'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        self.add_output_message(self.bot_handler.get_message(self.cmd_id, self.index))
        return self.exit_dfa


class DeleteCommandsMessageDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, cmd_id, index, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.index = index
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'index': self.index, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['index'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        self.bot_handler.remove_message(self.cmd_id, self.index)
        return self.exit_dfa


class SetCommandsMessageDFA(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'

    def __init__(self, chat_id, bot_handler, cmd_id, index, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message="Set a new output")
        self.cmd_id = cmd_id
        self.index = index
        self.set_command(self.CANCEL, exit_dfa)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'index': self.index, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['index'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        message = update.message
        if not message.has_non_empty_content():
            self.add_output_text(text="Current Message:")
            self.add_output_message(self.bot_handler.get_message(self.cmd_id, self.index))

    def process_input(self, update):
        message = update.message
        if message.has_non_empty_content():
            self.bot_handler.set_message(self.cmd_id, self.index, message)
            return self.exit_dfa


class ManageCommandsMessageDFA(TelegramDFADefinedCommands):
    BACK = u'⬅️'
    EDIT = 'Edit'
    DELETE = 'Delete'

    def __init__(self, chat_id, bot_handler, cmd_id, index, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.index = index
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'index': self.index, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['index'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        self.set_command(
            self.EDIT, SetCommandsMessageDFA(self.chat_id, self.bot_handler, self.cmd_id, self.index, self))
        self.set_command(
            self.DELETE,
            DeleteCommandsMessageDFA(self.chat_id, self.bot_handler, self.cmd_id, self.index, self.exit_dfa))
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.EDIT, self.DELETE, self.BACK]])
        self.set_message(
            "Command: " + self.bot_handler.get_command_name(self.cmd_id) + " Message: " + str(self.index + 1))


class CommandsMessagesDFA(TelegramDFADefinedCommands):
    BACK = u'⬅️'
    ADD_MESSAGE = 'Add Message'
    SET_RANDOM_MESSAGE = 'Enable Random Mode'
    SET_ALL_MESSAGES = 'Enable All Messages'

    def __init__(self, chat_id, bot_handler, cmd_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.exit_dfa = exit_dfa
        self.set_command(self.BACK, exit_dfa)

        self.set_command(self.SET_RANDOM_MESSAGE,
                         SetCustomCommandType(self.chat_id, self.bot_handler, cmd_id,
                                              CustomCommandType.RANDOM_MESSAGE, self))
        self.set_command(self.SET_ALL_MESSAGES,
                         SetCustomCommandType(self.chat_id, self.bot_handler, cmd_id,
                                              CustomCommandType.ALL_MESSAGES, self))

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        self.set_message("Manage messages of: " + self.bot_handler.get_command_path(self.cmd_id))
        self.set_command(self.ADD_MESSAGE, AddMessageToCommandDFA(self.chat_id, self.bot_handler, self.cmd_id, self))

        command_type = self.bot_handler.get_command_type(self.cmd_id)
        self.set_enable(self.SET_RANDOM_MESSAGE, command_type == CustomCommandType.ALL_MESSAGES)
        self.set_enable(self.SET_ALL_MESSAGES, command_type == CustomCommandType.RANDOM_MESSAGE)
        keyboard = [
            [self.ADD_MESSAGE],
            [self.SET_RANDOM_MESSAGE if command_type == CustomCommandType.ALL_MESSAGES else self.SET_ALL_MESSAGES],
        ]

        for command in self.get_command_names():
            dfa = self.get_command_dfa(command)
            if isinstance(dfa, ManageCommandsMessageDFA) or isinstance(dfa, ViewCommandsMessageOutputDFA):
                self.remove_command(command)
        for index in xrange(self.bot_handler.get_command_messages_count(self.cmd_id)):
            manage_name = "Message %d" % (index + 1)
            view_name = "Preview %d" % (index + 1)
            self.set_command(manage_name,
                             ManageCommandsMessageDFA(self.chat_id, self.bot_handler, self.cmd_id, index, self))
            self.set_command(view_name,
                             ViewCommandsMessageOutputDFA(self.chat_id, self.bot_handler, self.cmd_id, index, self))
            keyboard.append([manage_name, view_name])
        keyboard.append([self.BACK])
        self.set_keyboard(keyboard)


