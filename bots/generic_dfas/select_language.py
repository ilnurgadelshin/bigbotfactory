# -*- coding: utf-8 -*-

from bots.telegram_dfa import TelegramDFA
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands

from bots.libs.entities.user_state import UserState


class SupportedLanguages(object):
    ENGLISH = 'Eng'
    RUSSIAN = 'Рус'
    SPANISH = 'Esp'


class TelegramDFASetLanguage(TelegramDFA):
    def __init__(self, chat_id, bot_handler, language, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.language = language
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'language': self.language, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['language'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        UserState(self.chat_id).set_value('language', self.language)
        # self.bot_handler.user_context.set_value('language', self.language)
        text = "Your language was set to English"
        if self.language == SupportedLanguages.RUSSIAN:
            text = "Ваш язык был изменен на русский"
        if self.language == SupportedLanguages.SPANISH:
            text = "Su lengua se cambió"
        self.add_output_text(text)
        return self.exit_dfa


class TelegramDFASelectLanguages(TelegramDFADefinedCommands):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        keyboard = [[SupportedLanguages.ENGLISH, SupportedLanguages.RUSSIAN, SupportedLanguages.SPANISH], ['Cancel']]
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, 'Select your language', keyboard=keyboard)
        self.exit_dfa = exit_dfa
        self.set_command(SupportedLanguages.ENGLISH, TelegramDFASetLanguage(chat_id, bot_handler, SupportedLanguages.ENGLISH, exit_dfa))
        self.set_command(SupportedLanguages.RUSSIAN, TelegramDFASetLanguage(chat_id, bot_handler, SupportedLanguages.RUSSIAN, exit_dfa))
        self.set_command(SupportedLanguages.SPANISH, TelegramDFASetLanguage(chat_id, bot_handler, SupportedLanguages.SPANISH, exit_dfa))
        self.set_command('Cancel', exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, loader):
        return cls(
            loader.context['chat_id'],
            loader.context['bot_handler'],
            loader.load(dumped_object['exit_dfa']),
        )

    def process_input(self, update):
        pass
