import zlib
import base64

from boto3.dynamodb.conditions import Key

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables
from telegram.objects.message import TelegramMessage


class BotCustomCommands(object):
    NO_PARENT_ID = -1

    def __init__(self, bot_id):
        self.bot_id = bot_id

    def save_command(self, command_id, parent_id, command_name, messages, cmd_type, x, y):
        if parent_id is None:
            parent_id = BotCustomCommands.NO_PARENT_ID

        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        table.put_item(
           Item={
                'bot_id': self.bot_id,
                'command_id': command_id,
                'parent_id': parent_id,
                'info': {
                    'command_name': command_name,
                    'messages': map(lambda message: base64.b64encode(zlib.compress(message.to_json_str(), 1)), messages),
                    'cmd_type': cmd_type,
                    'parent_id': parent_id,
                    'x': x,
                    'y': y,
                }
            }
        )

    def remove_commands(self, list_of_command_ids):
        # I'm pretty sure it can be implemented in more efficient way,
        # but DynamoDB always writes in batch mode, so should be fine
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        for command_id in list_of_command_ids:
            table.delete_item(Key={'bot_id': self.bot_id, 'command_id': command_id})

    def has_command(self, cmd_id):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        response = table.get_item(Key={'bot_id': self.bot_id, 'command_id': cmd_id})
        return response.get('Item') is not None

    def get_command(self, cmd_id):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        response = table.get_item(Key={'bot_id': self.bot_id, 'command_id': cmd_id})
        if response.get('Item') is None:
            return None

        command = response.get('Item')['info']
        command['messages'] = map(
            lambda message_str: TelegramMessage.gen_from_json_str(zlib.decompress(base64.b64decode(message_str))),
            command['messages'],
        )
        return command

    def get_command_parent(self, cmd_id):
        command = self.get_command(cmd_id)
        if command is None:
            return None
        return command['parent_id']

    def get_child_commands(self, parent_id):
        if parent_id is None:
            parent_id = BotCustomCommands.NO_PARENT_ID
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        response = table.query(
            IndexName='parent_id-index',
            KeyConditionExpression=Key('bot_id').eq(self.bot_id) & Key('parent_id').eq(parent_id),
        )

        results = dict()
        for item in response[u'Items']:
            command_id = int(item['command_id'])
            results[command_id] = item['info']
            results[command_id]['messages'] = map(
                lambda message_str: TelegramMessage.gen_from_json_str(zlib.decompress(base64.b64decode(message_str))),
                results[command_id]['messages']
            )
        return results

    def set_command_name(self, cmd_id, name):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        table.update_item(
            Key={'bot_id': self.bot_id, 'command_id': cmd_id},
            UpdateExpression="set info.command_name = :v",
            ExpressionAttributeValues={':v': name},
        )

    def set_command_xy(self, cmd_id, x, y):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        table.update_item(
            Key={'bot_id': self.bot_id, 'command_id': cmd_id},
            UpdateExpression="set info.x = :x, info.y = :y",
            ExpressionAttributeValues={':x': x, ':y': y},
        )

    def set_command_type(self, cmd_id, cmd_type):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        table.update_item(
            Key={'bot_id': self.bot_id, 'command_id': cmd_id},
            UpdateExpression="set info.cmd_type" + " = :v",
            ExpressionAttributeValues={':v': cmd_type},
        )

    def get_command_messages(self, cmd_id):
        command = self.get_command(cmd_id)
        return command['messages']

    def get_command_message(self, cmd_id, index):
        messages = self.get_command_messages(cmd_id)
        if 0 <= index < len(messages):
            return messages[index]
        return None

    def set_command_messages(self, cmd_id, messages):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CUSTOM_COMMANDS)
        table.update_item(
            Key={'bot_id': self.bot_id, 'command_id': cmd_id},
            UpdateExpression="set info.messages = :v",
            ExpressionAttributeValues={
                ':v': map(lambda message: base64.b64encode(zlib.compress(message.to_json_str(), 1)), messages)},
        )


if __name__ == '__main__':
    import time
    commands = BotCustomCommands(1)
    commands.save_command(1, None, 'root', [TelegramMessage.gen_fake_text_message(1, "test")], 1, None, None)
    commands.save_command(2, 1, 'name1', [TelegramMessage.gen_fake_text_message(1, "test")], 1, None, None)
    commands.save_command(3, 1, 'name2', [], 1, 10, 10)
    time.sleep(1)
    print commands.get_command(1)
    print commands.get_command(2)
    print commands.get_command(3)
    print commands.get_child_commands(1)
    commands.remove_commands([2])
    print commands.get_command(1)
    print commands.get_command(2)
    print commands.get_command(3)
    print commands.get_child_commands(1)
