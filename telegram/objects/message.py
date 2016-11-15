# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.user import TelegramUser
from telegram.objects.chat import TelegramChat
from telegram.objects.audio import TelegramAudio
from telegram.objects.document import TelegramDocument
from telegram.objects.photo_size import TelegramPhotoSize
from telegram.objects.sticker import TelegramSticker
from telegram.objects.video import TelegramVideo
from telegram.objects.contact import TelegramContact
from telegram.objects.location import TelegramLocation
from telegram.objects.voice import TelegramVoice

import time


class TelegramMessage(TelegramObject):
    def __init__(self, message_id, from_, date, chat, forward_from=None, forward_date=None,
                 reply_to_message=None, text=None, audio=None, document=None, photo=None,
                 sticker=None, voice=None, video=None, caption=None, contact=None, location=None,
                 new_chat_participant=None, left_chat_participant=None, new_chat_title=None, new_chat_photo=None,
                 delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None,
                 channel_chat_created=None, migrate_to_chat_id=None, migrate_from_chat_id=None):
        assert message_id is not None
        assert date is not None
        assert chat is not None

        self.message_id = int(message_id)
        self.from_ = from_
        if from_ is not None:
            assert isinstance(from_, TelegramUser)
        self.date = int(date)
        self.chat = chat
        assert isinstance(chat, TelegramChat)

        self.forward_from = forward_from
        if forward_from is not None:
            assert isinstance(forward_from, TelegramUser)

        self.forward_date = int(forward_date) if forward_date is not None else None
        self.reply_to_message = reply_to_message
        if reply_to_message is not None:
            assert isinstance(reply_to_message, TelegramMessage)
        self.text = text

        self.audio = audio
        if audio is not None:
            assert isinstance(audio, TelegramAudio)

        self.document = document
        if document is not None:
            assert isinstance(document, TelegramDocument)

        self.photo = photo
        if photo is not None:
            for p in photo:
                assert isinstance(p, TelegramPhotoSize)

        self.sticker = sticker
        if sticker is not None:
            assert isinstance(sticker, TelegramSticker)

        self.video = video
        if video is not None:
            assert isinstance(video, TelegramVideo)

        self.voice = voice
        if voice is not None:
            assert isinstance(voice, TelegramVoice)

        self.caption = caption

        self.contact = contact
        if contact is not None:
            assert isinstance(contact, TelegramContact)

        self.location = location
        if location is not None:
            assert isinstance(location, TelegramLocation)

        self.new_chat_participant = new_chat_participant
        if new_chat_participant is not None:
            assert isinstance(new_chat_participant, TelegramUser)

        self.left_chat_participant = left_chat_participant
        if left_chat_participant is not None:
            assert isinstance(left_chat_participant, TelegramUser)

        self.new_chat_title = new_chat_title

        self.new_chat_photo = new_chat_photo
        if new_chat_photo is not None:
            for p in new_chat_photo:
                assert isinstance(p, TelegramPhotoSize)

        self.delete_chat_photo = bool(delete_chat_photo) if delete_chat_photo is not None else None
        self.group_chat_created = bool(group_chat_created) if group_chat_created is not None else None
        self.supergroup_chat_created = bool(supergroup_chat_created) if supergroup_chat_created is not None else None
        self.channel_chat_created = bool(channel_chat_created) if channel_chat_created is not None else None
        self.migrate_to_chat_id = int(migrate_to_chat_id) if migrate_to_chat_id is not None else None
        self.migrate_from_chat_id = int(migrate_from_chat_id) if migrate_from_chat_id is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        new_chat_photo = None
        if json_object.get('new_chat_photo') is not None:
            new_chat_photo = [TelegramPhotoSize.gen_from_json(p) for p in json_object['new_chat_photo']]
        forward_from = None
        if json_object.get('forward_from') is not None:
            forward_from = TelegramUser.gen_from_json(json_object['forward_from'])

        return TelegramMessage(
            message_id=json_object['message_id'],
            from_=TelegramUser.gen_from_json(json_object['from'])
                if json_object.get('from') is not None else None,
            date=json_object['date'],
            chat=TelegramChat.gen_from_json(json_object['chat']),
            forward_from=forward_from,
            forward_date=json_object.get('forward_date'),
            reply_to_message=TelegramMessage.gen_from_json(json_object['reply_to_message'])
                if json_object.get('reply_to_message') is not None else None,
            text=json_object.get('text'),
            audio=TelegramAudio.gen_from_json(json_object['audio'])
                if json_object.get('audio') is not None else None,
            document=TelegramDocument.gen_from_json(json_object['document'])
                if json_object.get('document') is not None else None,
            photo=[TelegramPhotoSize.gen_from_json(p) for p in json_object['photo']]
                if json_object.get('photo') is not None else None,
            sticker=TelegramSticker.gen_from_json(json_object['sticker'])
                if json_object.get('sticker') is not None else None,
            voice=TelegramVoice.gen_from_json(json_object['voice'])
                if json_object.get('voice') is not None else None,
            video=TelegramVideo.gen_from_json(json_object['video'])
                if json_object.get('video') is not None else None,
            caption=json_object.get('caption'),
            contact=TelegramContact.gen_from_json(json_object['contact'])
                if json_object.get('contact') is not None else None,
            location=TelegramLocation.gen_from_json(json_object['location'])
                if json_object.get('location') is not None else None,
            new_chat_participant=TelegramUser.gen_from_json(json_object['new_chat_participant'])
                if json_object.get('new_chat_participant') is not None else None,
            left_chat_participant=TelegramUser.gen_from_json(json_object['left_chat_participant'])
                if json_object.get('left_chat_participant') is not None else None,
            new_chat_title=json_object.get('new_chat_title'),
            new_chat_photo=new_chat_photo,
            delete_chat_photo=json_object.get('delete_chat_photo'),
            group_chat_created=json_object.get('group_chat_created'),
            supergroup_chat_created=json_object.get('supergroup_chat_created'),
            channel_chat_created=json_object.get('channel_chat_created'),
            migrate_to_chat_id=json_object.get('migrate_to_chat_id'),
            migrate_from_chat_id=json_object.get('migrate_from_chat_id'),
        )

    def to_json(self):
        result = {
            'message_id': self.message_id,
            'from': self.from_.to_json(),
            'date': self.date,
            'chat': self.chat.to_json(),
        }
        if self.forward_from is not None:
            result['forward_from'] = self.forward_from.to_json()
        if self.forward_date is not None:
            result['forward_date'] = self.forward_date
        if self.reply_to_message is not None:
            result['reply_to_message'] = self.reply_to_message.to_json()
        if self.text is not None:
            result['text'] = self.text
        if self.audio is not None:
            result['audio'] = self.audio.to_json()
        if self.document is not None:
            result['document'] = self.document.to_json()
        if self.photo is not None:
            result['photo'] = [photo.to_json() for photo in self.photo]
        if self.sticker is not None:
            result['sticker'] = self.sticker.to_json()
        if self.voice is not None:
            result['voice'] = self.voice.to_json()
        if self.video is not None:
            result['video'] = self.video.to_json()
        if self.caption is not None:
            result['caption'] = self.caption
        if self.contact is not None:
            result['contact'] = self.contact.to_json()
        if self.location is not None:
            result['location'] = self.location.to_json()
        if self.new_chat_participant is not None:
            result['new_chat_participant'] = self.new_chat_participant.to_json()
        if self.left_chat_participant is not None:
            result['left_chat_participant'] = self.left_chat_participant.to_json()
        if self.new_chat_title is not None:
            result['new_chat_title'] = self.new_chat_title
        if self.new_chat_photo is not None:
            result['new_chat_photo'] = [photo.to_json() for photo in self.new_chat_photo]
        if self.delete_chat_photo is not None:
            result['delete_chat_photo'] = self.delete_chat_photo
        if self.group_chat_created is not None:
            result['group_chat_created'] = self.group_chat_created
        if self.supergroup_chat_created is not None:
            result['supergroup_chat_created'] = self.supergroup_chat_created
        if self.channel_chat_created is not None:
            result['channel_chat_created'] = self.channel_chat_created
        if self.migrate_to_chat_id is not None:
            result['migrate_to_chat_id'] = self.migrate_to_chat_id
        if self.migrate_from_chat_id is not None:
            result['migrate_from_chat_id'] = self.migrate_from_chat_id
        return result

    def has_non_empty_content(self):
        attributes_to_check = ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'contact', 'location']
        for attr in attributes_to_check:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                return True
        return False

    @classmethod
    def gen_fake_text_message(cls, chat_id, text):
        user = TelegramUser(id=chat_id, first_name='FAKE USER')
        chat = TelegramChat(id=chat_id, type=TelegramChat.PRIVATE)
        return TelegramMessage(message_id=0, from_=user, chat=chat, date=time.time(), text=text)


if __name__ == '__main__':
    json_str = '{"message_id":956,"from":{"id":123456789,"first_name":"JOHN","last_name":"SMITH","username":"johnsmith"},"chat":{"id":123456789,"first_name":"JOHN","last_name":"SMITH","username":"johnsmith"},"date":1441651455,"audio":{"duration":53,"mime_type":"audio\/mpeg","title":"Aug 25, 16:21","performer":"beseda","file_id":"AQZDAQADGQAEfihIBU64KBb_H2q6Ag","file_size":214875}}'
    obj = TelegramMessage.gen_from_json_str(json_str)
    print obj.to_json()
    print obj.to_json_str()
    print obj.has_non_empty_content()
    print obj.audio
    print obj.audio.file_id
    print obj.message_id
    print obj.from_.first_name
    print obj.text
    print isinstance(obj.chat, TelegramUser)
    print obj.chat.last_name
    print obj.caption
