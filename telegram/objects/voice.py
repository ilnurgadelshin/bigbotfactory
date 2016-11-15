# -*- coding: utf-8 -*-

__author__ = 'ydudin'

from telegram.objects.telegram_object import TelegramObject


class TelegramVoice(TelegramObject):
    def __init__(self, file_id, duration, mime_type=None, file_size=None):
        assert file_id is not None
        assert duration is not None

        self.file_id = str(file_id)
        self.duration = int(duration)
        self.mime_type = mime_type
        self.file_size = int(file_size) if file_size is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramVoice(
            file_id=json_object['file_id'],
            duration=json_object['duration'],
            mime_type=json_object.get('mime_type'),
            file_size=json_object.get('file_size'),
        )

    def to_json(self):
        result = {
            'file_id': self.file_id,
            'duration': self.duration,
        }
        if self.mime_type is not None:
            result['mime_type'] = self.mime_type
        if self.file_size is not None:
            result['file_size'] = self.file_size
        return result


if __name__ == '__main__':
    obj = TelegramVoice.gen_from_json_str('{"file_id":"AgADAgADqacxKgfkjgndfjkihJKHUiQABFkRcB5hBNa1mC0AAgI","duration":15238, "file_size":160}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.file_id
    print obj.duration
    print obj.mime_type
    print obj.file_size