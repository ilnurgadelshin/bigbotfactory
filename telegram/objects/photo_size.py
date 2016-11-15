# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramPhotoSize(TelegramObject):
    def __init__(self, file_id, width, height, file_size=None):
        assert file_id is not None
        assert width is not None
        assert height is not None

        self.file_id = str(file_id)
        self.width = int(width)
        self.height = int(height)
        self.file_size = int(file_size) if file_size is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramPhotoSize(
            file_id=json_object['file_id'],
            width=json_object['width'],
            height=json_object['height'],
            file_size=json_object.get('file_size'),
        )

    def to_json(self):
        result = {
            'file_id': self.file_id,
            'width': self.width,
            'height': self.height,
            'file_size': self.file_size,
        }
        return result


if __name__ == '__main__':
    obj = TelegramPhotoSize.gen_from_json_str('{"file_id":"AgADAgADqacxG7t3pwFKzPtgWIqi0PVLAiQABFkRcB5hBNa1mC0AAgI","file_size":15238,"width":160,"height":160}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.file_id
    print obj.width
    print obj.height
    print obj.file_size