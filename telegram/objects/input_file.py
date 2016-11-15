# -*- coding: utf-8 -*-

class TelegramInputFile(object):
    def __init__(self, filepath):
        assert filepath is not None
        self.filepath = filepath

    def to_multipart(self):
        return open(self.filepath, 'rb')

