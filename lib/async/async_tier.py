import simplejson as json
from lib.globals.globals import Globals, GlobalParams
from lib.async.scheduled_async_jobs import ScheduledAsyncJobs
import boto3
import time


class AsyncTier(object):
    SEND_MESSAGE_ASYNC_ID = 1
    SEND_MESSAGES_ASYNC_ID = 2
    BROADCAST_TO_SUBSCRIBERS = 3

    _CLIENT = boto3.client('lambda')


    @classmethod
    def get_all_schedulable_async_ids(cls):
        return set(list([
            cls.BROADCAST_TO_SUBSCRIBERS,
        ]))

    @classmethod
    def send(cls, async_id, args, delay=None):
        """
        :param async_id: unique identifier
        :param args: a json-serializable object to be passed to some executor
        :param delay: time in seconds to delay async job execution. Job start time depends on cron job granularity
        :return: None
        """
        if delay is not None:
            assert async_id in cls.get_all_schedulable_async_ids()
            time_scheduled = time.time() + float(delay)
            ScheduledAsyncJobs.schedule_async_job(async_id, time_scheduled, args)

        data = json.dumps({'async_id': async_id, 'args': args, 'globals': Globals.dump_to_args()})
        cls._CLIENT.invoke(
            FunctionName='async_lambda__' + Globals.get(GlobalParams.API_VERSION_PARAM),
            InvocationType='Event',
            LogType='None',
            Payload=data,
        )

    @classmethod
    def get_executor(cls, async_id):
        raise NotImplementedError()

    @classmethod
    def execute_from_data(cls, data):
        async_id = data['async_id']
        executor = cls.get_executor(async_id)
        executor(data['args'])
