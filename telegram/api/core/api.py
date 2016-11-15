# -*- coding: utf-8 -*-

import requests

from telegram.api.core.connector import TelegramConnector
from telegram.objects.user import TelegramUser
from telegram.objects.message import TelegramMessage
from telegram.objects.user_profile_photos import TelegramUserProfilePhotos
from telegram.objects.reply_keyboard_markup import TelegramReplyKeyBoardMarkup
from telegram.objects.reply_keyboard_hide import TelegramReplyKeyBoardHide
from telegram.objects.force_reply import TelegramForceReply
from telegram.objects.input_file import TelegramInputFile
from telegram.objects.contact import TelegramContact
from telegram.objects.file import TelegramFile
from telegram.objects.telegram_response import TelegramResponse
from telegram.objects.inline_query_result import TelegramInlineQueryResult


class TelegramAPIHandler(object):
    def __init__(self, token):
        self._token = token
        self._id = int(token[:token.find(':')])

    def is_token(self, token):
        return token == self._token

    def get_bot_id(self):
        return self._id

    def get_me(self):
        # for bots username is always set and ends with 'bot'
        response = TelegramConnector.make_request(self._token, 'getMe')
        return TelegramUser.gen_from_json(response.result) if response.ok else None

    def get_token(self):
        return self._token

    def get_updates(self, offset, limit=100):
        params = {'limit': limit, 'offset': offset}
        response = TelegramConnector.make_request(self._token, 'getUpdates', params)
        return response.result if response.ok else None

    def send_message(self, chat_id, text, is_markdown=False, disable_web_page_preview=None, reply_to_message_id=None,
                     reply_markup=None, timeout=1.0):
        params = {'chat_id': chat_id, 'text': text}
        if disable_web_page_preview is not None:
            params['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if is_markdown:
            params['parse_mode'] = 'Markdown'
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendMessage', params, timeout=timeout)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    def forward_message(self, chat_id, from_chat_id, message_id):
        params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        response = TelegramConnector.make_request(self._token, 'forwardMessage', params)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(photo, basestring):
            params['photo'] = photo
        if isinstance(photo, TelegramInputFile):
            files['photo'] = photo.to_multipart()
        if caption is not None:
            params['caption'] = caption
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()

        response = TelegramConnector.make_request(self._token, 'sendPhoto', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    # according to the official documentation, this function only supports .mp3 files
    # For backward compatibility it also supports .ogg files encoded with OPUS, but it will be deprecated in the future
    def send_audio(self, chat_id, audio, duration=None, performer=None, title=None, reply_to_message_id=None,
                   reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(audio, basestring):
            params['audio'] = audio
        if isinstance(audio, TelegramInputFile):
            files['audio'] = audio.to_multipart()
        if duration is not None:
            params['duration'] = duration
        if performer is None:
            performer = "Telegram Audio"
        params['performer'] = performer
        if title is not None:
            params['title'] = title
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendAudio', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(document, basestring):
            params['document'] = document
        if isinstance(document, TelegramInputFile):
            files['document'] = document.to_multipart()
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendDocument', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    # must be in .webp or .jpg formats
    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(sticker, basestring):
            params['sticker'] = sticker
        if isinstance(sticker, TelegramInputFile):
            files['sticker'] = sticker.to_multipart()
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendSticker', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    # this function supports only mp4 video files, otherwise send them as documents
    def send_video(self, chat_id, video, duration=None, caption=None, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(video, basestring):
            params['video'] = video
        if isinstance(video, TelegramInputFile):
            files['video'] = video.to_multipart()
        if duration is not None:
            params['duration'] = duration
        if caption is not None:
            params['caption'] = caption
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendVideo', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    # this function supports .ogg files encoded with OPUS only
    def send_voice(self, chat_id, voice, duration=None, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id}
        files = {}
        if isinstance(voice, basestring):
            params['voice'] = voice
        if isinstance(voice, TelegramInputFile):
            files['voice'] = voice.to_multipart()
        if duration is not None:
            params['duration'] = duration
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendVoice', params, files)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if reply_to_message_id is not None:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            assert isinstance(reply_markup, TelegramReplyKeyBoardMarkup) or \
                   isinstance(reply_markup, TelegramReplyKeyBoardHide) or \
                   isinstance(reply_markup, TelegramForceReply)
            params['reply_markup'] = reply_markup.to_json_str()
        response = TelegramConnector.make_request(self._token, 'sendLocation', params)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response

    # action: [typing, upload_photo, record_video, upload_video, record_audio, upload_document, find_location]
    def send_chat_action(self, chat_id, action):
        params = {'chat_id': chat_id, 'action': action}
        return TelegramConnector.make_request(self._token, 'sendChatAction', params)

    def get_user_profile_photos(self, user_id, offset=None, limit=None):
        params = {'user_id': user_id}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        response = TelegramConnector.make_request(self._token, 'getUserProfilePhotos', params)
        if response.ok:
            response.result = TelegramUserProfilePhotos.gen_from_json(response.result)
        return response

    def send_telegram_contact(self, chat_id, contact):
        assert isinstance(contact, TelegramContact)
        last_name = ""
        if contact.last_name is not None:
            last_name = "\nLast name: " + contact.last_name + "\n"
        user_id = ""
        if contact.user_id is not None:
            user_id = "\nUser ID: " + str(contact.user_id)
        text = "Phone: " + contact.phone_number + "\nFirst name: " + contact.first_name + last_name + user_id
        return self.send_message(chat_id, text=text)

    def send_telegram_message(self, chat_id, message, reply_markup=None):
        assert isinstance(message, TelegramMessage)
        document_file_id = None
        response = None
        if message.text is not None:
            response = self.send_message(chat_id, message.text, reply_markup=reply_markup)

        if message.audio is not None:
            r = self.send_audio(chat_id, message.audio.file_id, reply_markup=reply_markup)
            if not r.ok:
                document_file_id = message.audio.file_id
            else:
                response = r
        if message.voice is not None:
            r = self.send_voice(chat_id, message.voice.file_id, reply_markup=reply_markup)
            if not r.ok:
                document_file_id = message.voice.file_id
            else:
                response = r
        if message.document is not None:
            document_file_id = message.document.file_id
        if message.photo is not None:
            response = self.send_photo(chat_id, message.photo[0].file_id, reply_markup=reply_markup)
        if message.sticker is not None:
            response = self.send_sticker(chat_id, message.sticker.file_id, reply_markup=reply_markup)
        if message.video is not None and hasattr(message.video, 'file_id') and getattr(message.video, 'file_id') is not None:
            r = self.send_video(chat_id, message.video.file_id, reply_markup=reply_markup)
            if not r.ok:
                document_file_id = message.video.file_id
            else:
                response = r
        if message.contact is not None:
            response = self.send_telegram_contact(chat_id, message.contact)
        if message.location is not None:
            response = self.send_location(chat_id, message.location.latitude, message.location.longitude,
                                          reply_markup=reply_markup)
        if document_file_id is not None:
            response = self.send_document(chat_id, document_file_id, reply_markup=reply_markup)
        if response is None:
            response = TelegramResponse(ok=False)
        return response

    def set_webhook(self, url):
        params = {'url': url}
        response = TelegramConnector.make_request(self._token, 'setWebhook', params)
        return response

    def get_file(self, file_id, filepath_to_save):
        params = {'file_id': file_id}
        response = TelegramConnector.make_request(self._token, 'getFile', params)
        if not response.ok:
            return False
        file = TelegramFile.gen_from_json(response.result)
        # convert response to File, curl file_path
        url = "https://api.telegram.org/file/bot" + self._token + "/" + file.file_path
        request = requests.get(url, stream=True)
        with open(filepath_to_save, 'w') as result_file:
            result_file.write(request.content)
        result_file.close()
        return True

    def answer_inline_query(self, inline_query_id, results, cache_time=None, is_personal=False, next_offset=None):
        jsoned_results = []
        for r in results:
            assert isinstance(r, TelegramInlineQueryResult)
            if len(jsoned_results) < 50:
                jsoned_results.append(r.to_json())
        params = {'inline_query_id': inline_query_id, 'results': jsoned_results, 'is_personal': is_personal}
        if cache_time is not None:
            params['cache_time'] = cache_time
        if next_offset is not None:
            params['next_offset'] = next_offset
        response = TelegramConnector.make_request(self._token, 'answerInlineQuery', params)
        if response.ok:
            response.result = TelegramMessage.gen_from_json(response.result)
        return response