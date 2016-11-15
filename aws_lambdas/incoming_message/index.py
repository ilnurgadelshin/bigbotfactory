from __future__ import print_function

import traceback
import pprint
from telegram.objects.update import TelegramUpdate
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot

from bots.bots_factory import BotsFactory
from bots.bot_handler import BotHandler
from lib.globals.globals import Globals


def lambda_handler(event, context):
    """Used for handling incoming messages for general bot handler"""
    update = None
    try:
        Globals.initialize_from_args(event)
        token = event['token']
        update = TelegramUpdate.gen_from_json_str(event['update_str'])
        BBFAlarmBot.set_prefix('Alarm from bot with token: ' + token + '\n')
        bot_handler = BotsFactory.get_by_name(event['bot_handler'])
        assert issubclass(bot_handler, BotHandler)
        bot_handler = bot_handler(event['token'], update)
        bot_handler.process()
    except:
        trace = traceback.format_exc()
        try:
            text = "Event Exception: can't proceed event: " + str(event) + " with a trace:\n" + str(trace)
            if update is not None:
                text = "Bot Handler Exception for update_id: " + str(update.update_id) + " trace:\n" + str(trace)
            BBFAlarmBot.alarm_developers(text)
        except:
            pprint.pprint(
                "can't send a message to developers! event: ", event, "\ntrace: ", str(traceback.format_exc()))
        pprint.pprint(trace)
    return "ok"