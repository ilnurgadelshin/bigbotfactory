from __future__ import print_function

from aws_telegram.aws_api_handler import AWSAsyncTier
from lib.async.async_tier import AsyncTier, ScheduledAsyncJobs
import pprint
import traceback
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot
from lib.globals.globals import Globals
import time


def lambda_handler(event, context):
    traces = []
    try:
        current_time = time.time()
        for async_id in AsyncTier.get_all_schedulable_async_ids():
            jobs = ScheduledAsyncJobs.find_all_scheduled_jobs(async_id, current_time)
            for timestamp, job in jobs.iteritems():
                try:
                    args = job[1]
                    globals_args = job[2]
                    Globals.initialize_from_args(globals_args)
                    AWSAsyncTier.execute_from_data({
                        'async_id': async_id,
                        'args': args
                    })
                except:
                    traces.append(
                        "Execution for async_id: " + str(async_id) + " timestamp: " + str(timestamp) +
                        " failed:" + traceback.format_exc())
                finally:
                    ScheduledAsyncJobs.delete_job(async_id, timestamp)
    except:
        trace = traceback.format_exc()
        try:
            text = "Event Exception: can't proceed event: " + str(event) + " with a trace:\n" + str(trace)
            BBFAlarmBot.alarm_developers(text)
        except:
            pprint.pprint(
                "can't send a message to developers! event: ", event, "\ntrace: ", str(traceback.format_exc()))
        pprint.pprint(trace)
    if len(traces):
        BBFAlarmBot.alarm_developers("Scheduled async started failed:\n" + "\n".join(traces))
    return "ok"