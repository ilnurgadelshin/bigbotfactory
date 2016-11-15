from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands


class TelegramDFAConfirm(TelegramDFADefinedCommands):
    def __init__(self, chat_id, bot_handler, confirm_dfa, no_dfa, default_text='Please confirm your operation',
                 confirm_text='Confirm', no_text='Cancel'):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler, default_message=default_text)
        self.confirm_dfa = confirm_dfa
        self.no_dfa = no_dfa
        self.default_text = default_text
        self.confirm_text = confirm_text
        self.no_text = no_text


    def _intern_dump(self, existing_ids):
        return {'confirm_dfa': self.confirm_dfa.dump(existing_ids),
                'no_dfa': self.no_dfa.dump(existing_ids),
                'default_text': self.default_text,
                'confirm_text': self.confirm_text,
                'no_text': self.no_text}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['confirm_dfa'], context),
            cls.load(dumped_object['no_dfa'], context),
            dumped_object['default_text'],
            dumped_object['confirm_text'],
            dumped_object['no_text'],
        )

    def update_menu(self, update):
        self.set_command(self.confirm_text, self.confirm_dfa)
        self.set_command(self.no_text, self.no_dfa)
        self.set_keyboard([[self.confirm_text, self.no_text]])
