from telegram.objects.update import TelegramUpdate, TelegramMessage
from bots.bot_handler import BotHandler
from lib.dfa.dfa import DFA


class TelegramDFAGoToInitialDFAException(Exception): pass


class TelegramDFA(DFA):
    def __init__(self, chat_id, bot_handler, start_dfa=None):
        DFA.__init__(self, start_dfa=start_dfa)
        self.chat_id = chat_id  # every telegram dfa belongs to some chat
        self.bot_handler = bot_handler
        isinstance(self.bot_handler, BotHandler)

    def _fix_update_on_change(self, update):
        message = update.message
        assert isinstance(message, TelegramMessage)
        # there can be different strategies, but for most cases, a reduced update should work well
        return TelegramUpdate(
            update_id=update.update_id,
            message=TelegramMessage(
                message_id=message.message_id,
                date=message.date,
                chat=message.chat,
                from_=message.from_))

    def assert_update(self, update):
        isinstance(update, TelegramUpdate)

    def add_output_message(self, message):
        self.bot_handler.add_output_message(message)

    def add_output_text(self, text):
        self.bot_handler.add_output_text(text)

    def set_output_reply(self, reply):
        self.bot_handler.set_output_reply(reply)
