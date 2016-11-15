# -*- coding: utf-8 -*-

from bots.dfa_bot_handler import DFABotHandler
from bots.bbfbot.bbf_dfa import BBFDFA
from lib.globals.globals import Globals, GlobalParams


class BBFHandler(DFABotHandler):
    def __init__(self, token, update):
        DFABotHandler.__init__(self, token, update)
        self.web_hook = 'https://balancer.example.com/bots/' + Globals.get(GlobalParams.API_VERSION_PARAM)

    def process_on_given_token(self):
        return True

    def _initial_dfa(self):
        return BBFDFA(self.chat_id, self)


if __name__ == '__main__':
    from telegram.objects.update import TelegramUpdate
    from telegram.objects.message import TelegramMessage
    from telegram.api.core.api import TelegramAPIHandler
    import datetime

    chat_id = 123456789
    token = '*'
    debug_api_handler = TelegramAPIHandler(token)
    messages = [
        'hi',
        'My bots',
        'test05robot',
    ]
    debug_api_handler.send_message(chat_id, 'Starting a new test: ' + str(datetime.datetime.now()))
    for m in messages:
        debug_api_handler.send_message(chat_id, 'Received a message:\n' + m)
        update = TelegramUpdate(chat_id, TelegramMessage.gen_fake_text_message(chat_id, m))
        handler = BBFHandler(token, update)
        handler.process()
