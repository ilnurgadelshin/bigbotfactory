# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.photo_size import TelegramPhotoSize


class TelegramUserProfilePhotos(TelegramObject):
    def __init__(self, total_count, photos):
        assert total_count is not None
        assert photos is not None

        self.total_count = int(total_count)
        assert isinstance(photos, list) or isinstance(photos, tuple)
        for photos_by_size in photos:
            assert isinstance(photos_by_size, list) or isinstance(photos_by_size, tuple)
            for photo in photos_by_size:
                assert isinstance(photo, TelegramPhotoSize)
        self.photos = photos


    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramUserProfilePhotos(
            total_count=json_object['total_count'],
            photos=[[TelegramPhotoSize.gen_from_json(photo)
                     for photo in photos_by_size] for photos_by_size in json_object['photos']]
        )

    def to_json(self):
        result = {
            'total_count': self.total_count,
            'photos': [[photo.to_json() for photo in photos_by_size] for photos_by_size in self.photos]
        }
        return result


if __name__ == '__main__':
    string = '{"total_count": 1, "photos": [[{"file_id": "AgADAgADqacxG7t3pwFKnfjkgfdgHGABFkRcB5hBNa1mC0AAgI", "file_size": 15238, "width": 160, "height": 160}, {"file_id": "AgADAgADqacxG7t3pwFKGjkfbgjHS0AAgI", "file_size": 48339, "width": 320, "height": 320}], [{"file_id": "AgADAgADqacxG7t3pwFKzPNKJnkjgnfjgBABNlFBCGqsZ3Umi0AAgI", "file_size": 149318, "width": 640, "height": 640}]]}'
    obj = TelegramUserProfilePhotos.gen_from_json_str(string)
    print obj.to_json()
    print string
    print obj.to_json_str()
    print obj.total_count
    print obj.photos
