from bots.telegram_dfa import TelegramDFA
from bots.libs.entities.bot_subscribers import BotSubscribers


class BotStatsDFA(TelegramDFA):
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
        count = BotSubscribers(self.bot_handler.api_handler.get_bot_id()).get_subscribers_count()
        self.add_output_text("Total subscribers: " + str(count))
        return self.exit_dfa
