# -*- coding: utf-8 -*-

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables
from lib.globals.globals import Globals, GlobalParams
import random
from boto3.dynamodb.conditions import Key
from decimal import Decimal


class ScheduledAsyncJobs(object):
    @classmethod
    def schedule_async_job(cls, async_id, time_scheduled, args):
        table = DynamoDB.get_table(DynamoDBTables.SCHEDULED_ASYNC_JOBS)
        job_id = random.randint(1000, 100000000)
        table.put_item(
            Item={
                'async_id': async_id,
                'timestamp': Decimal(time_scheduled),
                'info': {
                    'job_id': int(job_id),
                    'args': args,
                    'globals': Globals.dump_to_args()
                }
            })

    @classmethod
    def find_all_scheduled_jobs(cls, async_id, timestamp):
        table = DynamoDB.get_table(DynamoDBTables.SCHEDULED_ASYNC_JOBS)
        response = table.query(
            KeyConditionExpression=Key('async_id').eq(async_id) & Key('timestamp').lte(Decimal(timestamp)),
        )

        results = dict()
        for item in response[u'Items']:
            info = item['info']
            results[item['timestamp']] = (int(info['job_id']), info['args'], info['globals'])
        return results

    @classmethod
    def delete_job(cls, async_id, timestamp):
        table = DynamoDB.get_table(DynamoDBTables.SCHEDULED_ASYNC_JOBS)
        table.delete_item(Key={'async_id': async_id, 'timestamp': Decimal(timestamp)})


if __name__ == '__main__':
    Globals.set(GlobalParams.API_VERSION_PARAM, 'beta')
    import time
    current_time = time.time()
    ScheduledAsyncJobs.schedule_async_job(1, current_time - 10, {'text': 'text1'})
    ScheduledAsyncJobs.schedule_async_job(1, current_time, {'text': 'text2'})
    ScheduledAsyncJobs.schedule_async_job(1, current_time + 10, {'text': 'text3'})
    print ScheduledAsyncJobs.find_all_scheduled_jobs(2, current_time)
    for timestamp, job in ScheduledAsyncJobs.find_all_scheduled_jobs(1, current_time + 5).iteritems():
        print timestamp, job
        ScheduledAsyncJobs.delete_job(1, timestamp)
    time.sleep(1)
    print ScheduledAsyncJobs.find_all_scheduled_jobs(1, current_time + 10)



