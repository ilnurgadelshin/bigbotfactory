# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.photo_size import TelegramPhotoSize


class TelegramDocument(TelegramObject):
    def __init__(self, file_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        assert file_id is not None

        self.file_id = str(file_id)
        self.thumb = thumb
        if self.thumb is not None:
            assert isinstance(self.thumb, TelegramPhotoSize)
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = int(file_size) if file_size is not None else None



    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramDocument(
            file_id=json_object['file_id'],
            thumb=TelegramPhotoSize.gen_from_json(
                json_object['thumb']) if json_object.get('thumb') is not None else None,
            file_name=json_object.get('file_name'),
            mime_type=json_object.get('mime_type'),
            file_size=json_object.get('file_size'),
        )

    def to_json(self):
        result = {'file_id': self.file_id}
        if self.thumb is not None:
            result['thumb'] = self.thumb.to_json()
        if self.file_name is not None:
            result['file_name'] = self.file_name
        if self.mime_type is not None:
            result['mime_type'] = self.mime_type
        if self.file_size is not None:
            result['file_size'] = self.file_size
        return result


if __name__ == '__main__':
    pz = TelegramPhotoSize(file_id="AgADAgADqacxH3pwFAKzPtAAgWIqi0PVLAiQABFkRcB5hBNa1mC0AAgI", width=10, height=10)
    obj = TelegramDocument.gen_from_json_str('{"file_id":"AgADAgADqacxG7t3pwFKzPtJdfdUnjkhsgscB5hBNa1mC0AAgI","thumb":%s, "file_name": "/home/john/smth", "file_size":160}' % pz.to_json_str())
    print obj.to_json()
    obj2 = TelegramDocument.gen_from_json(obj.to_json())
    print obj2.to_json_str()
    print obj2.file_id
    print obj2.thumb.to_json_str()
    print obj2.file_name
    print obj2.mime_type
    print obj2.file_size
