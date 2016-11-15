# -*- coding: utf-8 -*-
import re
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands, TelegramDFA


class AddChannelsDFA(TelegramDFADefinedCommands):
    BACK = u'⬅️'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Enter the name:')
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

    def update_menu(self, update):
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.BACK]])

    def process_input(self, update):
        if len(self.bot_handler.get_channels()) >= 20:
            self.add_output_text(text='Sorry, you cannot add more than 20 channels')
            return self.exit_dfa
        text = update.message.text
        if text:
            if not re.match("^[a-z0-9_]*$", text):
                self.add_output_text(text='Sorry, the name is invalid, you can use a-z, 0-9 and underscores')
                return
            if len(text) > 50:
                self.add_output_text(text='Sorry, the name is too long')
                return
            if len(text) < 5:
                self.add_output_text(text='Sorry, the name is too short')
                return
            self.bot_handler.add_channel(text.strip())
            return self.exit_dfa


class DeleteChannelDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, channel_name, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa
        self.channel_name = channel_name

    def _intern_dump(self, existing_ids):
        return {'channel_name': self.channel_name, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['channel_name'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        self.bot_handler.remove_channel(self.channel_name)
        return self.exit_dfa


class ViewChannelsDFA(TelegramDFADefinedCommands):
    DELETE = 'Delete'
    BACK = u'⬅️'

    def __init__(self, chat_id, bot_handler, channel_name, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Channel: ' + channel_name)
        self.exit_dfa = exit_dfa
        self.channel_name = channel_name

    def _intern_dump(self, existing_ids):
        return {'channel_name': self.channel_name, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['channel_name'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def update_menu(self, update):
        self.set_command(
            self.DELETE,
            DeleteChannelDFA(self.chat_id, self.bot_handler, self.channel_name, self.exit_dfa))
        self.set_command(self.BACK, self.exit_dfa)
        self.set_keyboard([[self.DELETE, self.BACK]])


class ChannelsModule(TelegramDFADefinedCommands):
    ADD_CHANNEL = 'Add a channel'
    BACK = u'⬅️'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Channels:')
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

    def update_menu(self, update):
        self.set_command(self.ADD_CHANNEL, AddChannelsDFA(self.chat_id, self.bot_handler, self))
        self.set_command(self.BACK, self.exit_dfa)
        keyboard = [[self.ADD_CHANNEL]]
        for channel in self.bot_handler.get_channels():
            self.set_command(channel, ViewChannelsDFA(self.chat_id, self.bot_handler, channel, self))
            keyboard.append([channel])
        keyboard.append([self.BACK])
        self.set_keyboard(keyboard)
