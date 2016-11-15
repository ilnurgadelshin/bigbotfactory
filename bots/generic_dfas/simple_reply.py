from bots.telegram_dfa import TelegramDFA


class TelegramDFASimpleReply(TelegramDFA):
    def __init__(self, chat_id, bot_handler, text, exit_dfa):
        TelegramDFA.__init__(self, chat_id=chat_id, bot_handler=bot_handler)
        self.text = text
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'text': self.text, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['text'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        self.add_output_text(self.text)
        return self.exit_dfa
