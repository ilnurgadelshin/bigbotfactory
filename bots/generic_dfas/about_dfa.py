# -*- coding: utf-8 -*-

from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands


class TelegramDFAAbout(TelegramDFADefinedCommands):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message='')
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

    def process_input(self, update):
        self.bot_handler.show_about()
        return self.exit_dfa


class TelegramDFASetAbout(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message='Set New About:')
        self.exit_dfa = exit_dfa
        self.set_command(self.CANCEL, self.exit_dfa)
        self.set_keyboard([[self.CANCEL]])

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def process_input(self, update):
        self.bot_handler.show_about()
        text = update.message.text
        if text:
            new_about = text.strip()
            self.bot_handler.set_about(new_about)
            self.add_output_text('New about was set')
            return self.exit_dfa
