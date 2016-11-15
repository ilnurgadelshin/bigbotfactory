# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramFile(TelegramObject):
    def __init__(self, file_id, file_size=None, file_path=None):
        assert file_id is not None
        self.file_id = str(file_id)

        self.file_size = int(file_size) if file_size is not None else None
        self.file_path = file_path

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramFile(
            file_id=json_object['file_id'],
            file_size=json_object.get('file_size'),
            file_path=json_object.get('file_path'))

    def to_json(self):
        result = {'file_id': self.file_id}
        if self.file_size is not None:
            result['file_size'] = self.file_size
        if self.file_path is not None:
            result['file_path'] = self.file_path
        return result


if __name__ == '__main__':
    obj = TelegramFile.gen_from_json_str('{"file_id": "BQADAgADhIHDfngdHJWg2HyLGx-QsAg"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.file_id