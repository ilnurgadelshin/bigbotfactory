# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.photo_size import TelegramPhotoSize


class TelegramSticker(TelegramObject):
    def __init__(self, file_id, width, height, thumb=None, file_size=None):
        assert file_id is not None
        assert width is not None
        assert height is not None

        self.file_id = str(file_id)
        self.width = int(width)
        self.height = int(height)
        self.thumb = thumb
        if self.thumb is not None:
            assert isinstance(self.thumb, TelegramPhotoSize)
        self.file_size = int(file_size) if file_size is not None else None



    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramSticker(
            file_id=json_object['file_id'],
            width=json_object['width'],
            height=json_object['height'],
            thumb=TelegramPhotoSize.gen_from_json(
                json_object['thumb']) if json_object.get('thumb') is not None else None,
            file_size=json_object.get('file_size'),
        )

    def to_json(self):
        result = {'file_id': self.file_id, 'width': self.width, 'height': self.height}
        if self.thumb is not None:
            result['thumb'] = self.thumb.to_json()
        if self.file_size is not None:
            result['file_size'] = self.file_size
        return result


if __name__ == '__main__':
    pz = TelegramPhotoSize(file_id="AgADAgADqacfgjdfhgHKJABFkRcB5hBNa1mC0AAgI", width=10, height=10)
    obj = TelegramSticker.gen_from_json_str('{"file_id":"AgADAgADqacxG7t3pwFKzjgkfgjdfoigjHQABFkRcB5hBNa1mC0AAgI","width": 100, "height": 200, "thumb":%s, "file_size":160}' % pz.to_json_str())
    print obj.to_json()
    obj2 = TelegramSticker.gen_from_json(obj.to_json())
    print obj2.to_json_str()
    print obj2.file_id
    print obj2.width
    print obj2.height
    print obj2.thumb.to_json_str()
    print obj2.file_size
