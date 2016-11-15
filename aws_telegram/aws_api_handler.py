# -*- coding: utf-8 -*-

from lib.async.async_tier import AsyncTier
from telegram.api.core.api import TelegramAPIHandler
from telegram.objects.telegram_response import TelegramResponse
from telegram.objects.message import TelegramMessage
from telegram.objects.reply_keyboard_markup import TelegramReplyKeyBoardMarkup
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot

import time


class AWSAsyncTier(AsyncTier):
    @classmethod
    def get_executor(cls, async_id):
        if async_id == cls.SEND_MESSAGE_ASYNC_ID:
            return TelegramAWSAPIHandler.send_message_async_executor
        if async_id == cls.SEND_MESSAGES_ASYNC_ID:
            return TelegramAWSAPIHandler.send_telegram_messages_executor
        raise NotImplementedError()


class TelegramAWSAPIHandler(TelegramAPIHandler):
    def send_message_async(self, chat_id, message):
        AWSAsyncTier.send(
            AWSAsyncTier.SEND_MESSAGE_ASYNC_ID,
            {'text': message, 'token': self._token, 'chat_id': chat_id}
        )

    @classmethod
    def send_message_async_executor(cls, args):
        text = args['text']
        token = args['token']
        api_handler = TelegramAPIHandler(token)
        api_handler.send_message(int(args['chat_id']), text)

    def send_telegram_messages(self, chat_id_or_ids, messages, reply_markup=None, async=True,
                               send_stats_to_chat_ids=None):  # send_stats_to should be a list of chat_ids
        if isinstance(chat_id_or_ids, int):
            chat_id_or_ids = [chat_id_or_ids]
        if len(chat_id_or_ids) == 0 or len(messages) == 0:
            return

        messages = [TelegramMessage.gen_from_json_str(m) if isinstance(m, basestring) else m for m in messages]
        if async:
            AWSAsyncTier.send(AWSAsyncTier.SEND_MESSAGES_ASYNC_ID, {
                'token': self._token,
                'chat_ids': list(chat_id_or_ids),
                'messages': [m.to_json_str() for m in messages],
                'reply_markup': reply_markup.to_json_str() if reply_markup is not None else None,
                'send_stats_to_chat_ids': send_stats_to_chat_ids,
            })
            return

        ONT_TIME_TO_SLEEP = 2.0
        total_slept_time = 0
        stats = {
            'muted': {'users': 0, 'chats': 0},
            'ok': {'users': 0, 'chats': 0},
            'other': {'users': 0, 'chats': 0},
        }
        have_to_sleep = False
        for chat_id in chat_id_or_ids:
            if have_to_sleep:
                # that's dangerous, each lambda has its own timeout
                total_slept_time += ONT_TIME_TO_SLEEP
                time.sleep(ONT_TIME_TO_SLEEP)
                have_to_sleep = False

            status = 'ok'
            for message in messages:
                response = self.send_telegram_message(chat_id, message, reply_markup=reply_markup)
                if not response.ok:
                    status = 'other'
                    if response.error_code == TelegramResponse.ERROR_CODE_KICKED_FROM_CHAT:
                        status = 'muted'
                        break  # bot was stopped, no need in sending other messages
                    if response.error_code == TelegramResponse.ERROR_CODE_EXCEPTION:
                        have_to_sleep = True
                    break
            if chat_id > 0:
                stats[status]['users'] += 1
            else:
                stats[status]['chats'] += 1
        if send_stats_to_chat_ids:
            text = u"Total: %d\n" % len(chat_id_or_ids)
            text += u"Ok: %d users 👤 + %d chats 👥\n" % (stats['ok']['users'], stats['ok']['chats'])
            text += u"Muted: %d users 👤 + %d chats 👥\n" % \
                   (stats['muted']['users'] + stats['other']['users'],
                    stats['muted']['chats'] + + stats['other']['chats'])
            message = TelegramMessage.gen_fake_text_message(0, text)
            for send_stats_to_chat_id in send_stats_to_chat_ids:
                self.send_telegram_message(send_stats_to_chat_id, message)
        if total_slept_time > 0:
            BBFAlarmBot.alarm_developers("Bot with token: " + self._token + " slept: " + str(total_slept_time))

    @classmethod
    def send_telegram_messages_executor(cls, args):
        token = args['token']
        api_handler = TelegramAWSAPIHandler(token)
        messages = [TelegramMessage.gen_from_json_str(m) for m in args['messages']]
        reply_markup = None
        if args.get('reply_markup') is not None:
            reply_markup = TelegramReplyKeyBoardMarkup.gen_from_json_str(args['reply_markup'])
        api_handler.send_telegram_messages(
            args['chat_ids'], messages, async=False, reply_markup=reply_markup,
            send_stats_to_chat_ids=args.get('send_stats_to_chat_ids'))