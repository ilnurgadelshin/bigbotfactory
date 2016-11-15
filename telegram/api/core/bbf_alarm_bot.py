"""
THIS IS NOT A HANDLER BUT A HARDCODED BOT USED FOR ALARMING
"""
import sys
from telegram.api.core.connector import TelegramConnector


class BBFAlarmBot(object):
    TOKEN = "YOUR_TOKEN"
    NAME = "bbf_alarm_bot"

    DEVELOPERS = [123456789, 987654321]
    PREFIX = None

    @classmethod
    def set_developers(cls, developers):
        cls.DEVELOPERS = developers

    @classmethod
    def set_prefix(cls, prefix):
        cls.PREFIX = prefix

    @classmethod
    def alarm_developers(cls, text):
        prefix = '' if cls.PREFIX is None else cls.PREFIX
        try:
            while text:
                sub_text = prefix + "\n" + text[:5000]
                for developer_id in cls.DEVELOPERS:
                    params = {'chat_id': developer_id, 'text': sub_text}
                    TelegramConnector.make_request(cls.TOKEN, 'sendMessage', params, timeout=None)
                text = text[5000:]
        except:
            print >> sys.stderr, prefix, text


