from __future__ import print_function

from aws_telegram.aws_api_handler import AWSAsyncTier
import pprint
import traceback
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot
from lib.globals.globals import Globals


def lambda_handler(event, context):
    try:
        Globals.initialize_from_args(event['globals'])
        AWSAsyncTier.execute_from_data(event)
    except:
        trace = traceback.format_exc()
        try:
            text = "Event Exception: can't proceed event: " + str(event) + " with a trace:\n" + str(trace)
            BBFAlarmBot.alarm_developers(text)
        except:
            pprint.pprint(
                "can't send a message to developers! event: ", event, "\ntrace: ", str(traceback.format_exc()))
        pprint.pprint(trace)
    return "ok"