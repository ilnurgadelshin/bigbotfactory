import time
from decimal import Decimal

from boto3.dynamodb.conditions import Key

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class BotSubscriberStatus(object):
    SUBSCRIBED = 1
    UNSUBSCRIBED = 2


class BotSubscribers(object):
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def _set_status(self, chat_id, status, timestamp=None):
        # TODO: this function can be run async-ly for better performance
        table = DynamoDB.get_table(DynamoDBTables.BOTS_SUBSCRIBERS)
        table.put_item(
           Item={
                'bot_id': self.bot_id,
                'chat_id': chat_id,
                'info': {
                    'status': status,
                    'timestamp': timestamp if timestamp is not None else Decimal(time.time()),
                }
            }
        )

    def subscribe(self, chat_id):
        self._set_status(chat_id, BotSubscriberStatus.SUBSCRIBED)

    def unsubscribe(self, chat_id):
        self._set_status(chat_id, BotSubscriberStatus.UNSUBSCRIBED)

    def get_subscription(self, chat_id):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_SUBSCRIBERS)
        response = table.get_item(Key={'bot_id': self.bot_id, 'chat_id': chat_id})
        item = response.get('Item')
        if item is None:
            return None
        return item['info']['status']

    def get_all_subscribers(self):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_SUBSCRIBERS)
        response = table.query(
            KeyConditionExpression=Key('bot_id').eq(self.bot_id),
        )

        results = set()
        for item in response[u'Items']:
            if int(item['info']['status']) == BotSubscriberStatus.SUBSCRIBED:
                results.add(int(item['chat_id']))
        return results

    def get_subscribers_count(self):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_SUBSCRIBERS)
        response = table.query(
            KeyConditionExpression=Key('bot_id').eq(self.bot_id),
            Select='COUNT',
        )
        return int(response['Count'])



if __name__ == '__main__':
    bot_subscribers = BotSubscribers(1)
    bot_subscribers.subscribe(2)
    bot_subscribers.subscribe(3)
    print bot_subscribers.get_subscription(1)
    print bot_subscribers.get_subscription(2)
    print bot_subscribers.get_subscription(3)
    print bot_subscribers.get_all_subscribers()
    print bot_subscribers.get_subscribers_count()
    bot_subscribers.unsubscribe(2)
    print bot_subscribers.get_subscription(1)
    print bot_subscribers.get_subscription(2)
    print bot_subscribers.get_subscription(3)
    print bot_subscribers.get_all_subscribers()
    print bot_subscribers.get_subscribers_count()
