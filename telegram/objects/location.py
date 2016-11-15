# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramLocation(TelegramObject):
    def __init__(self, longitude, latitude):
        assert longitude is not None
        assert latitude is not None

        self.longitude = float(longitude)
        self.latitude = float(latitude)

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramLocation(
            longitude=json_object['longitude'],
            latitude=json_object['latitude'],
        )

    def to_json(self):
        result = {
            'longitude': self.longitude,
            'latitude': self.latitude,
        }
        return result


if __name__ == '__main__':
    obj = TelegramLocation.gen_from_json_str('{"longitude": 0.7, "latitude": 0.4}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.longitude
    print obj.latitude