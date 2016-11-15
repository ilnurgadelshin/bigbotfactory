from bots.telegram_dfa import TelegramDFA, TelegramDFAGoToInitialDFAException


class TelegramDFAGoToRoot(TelegramDFA):
    def __init__(self, chat_id, bot_handler):
        TelegramDFA.__init__(self, chat_id=chat_id, bot_handler=bot_handler)

    def _intern_dump(self, existing_ids):
        return {}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
        )

    def on_terminate(self, update):
        raise TelegramDFAGoToInitialDFAException()
