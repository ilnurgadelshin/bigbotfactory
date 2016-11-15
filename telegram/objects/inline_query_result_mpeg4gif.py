# -*- coding: utf-8 -*-

from telegram.objects.inline_query_result import TelegramInlineQueryResult


class TelegramInlineQueryResultMPEG4GIF(TelegramInlineQueryResult):
    def __init__(self, id_, mpeg4_url, mpeg4_width=None, mpeg4_height=None, thumb_url=None, title=None,
                 caption=None, message_text=None, parse_mode=None, disable_web_page_preview=False):
        assert id_ is not None
        assert mpeg4_url is not None

        self.type = "mpeg4_gif"
        self.id_ = id_
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = int(mpeg4_width) if mpeg4_width is not None else None
        self.mpeg4_height = int(mpeg4_height) if mpeg4_height is not None else None
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.message_text = message_text
        assert parse_mode is None or parse_mode == "Markdown"
        self.parse_mode = parse_mode
        assert isinstance(disable_web_page_preview, bool)
        self.disable_web_page_preview = bool(disable_web_page_preview)

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramInlineQueryResultMPEG4GIF(
            id_=json_object['id'],
            mpeg4_url=json_object['mpeg4_url'],
            mpeg4_width=json_object.get('mpeg4_width'),
            mpeg4_height=json_object.get('mpeg4_height'),
            thumb_url=json_object.get('thumb_url'),
            title=json_object.get('title'),
            caption=json_object.get('caption'),
            message_text=json_object.get('message_text'),
            parse_mode=json_object.get('parse_mode'),
            disable_web_page_preview=bool(json_object.get('disable_web_page_preview')),
        )

    def to_json(self):
        result = {'type': self.type, 'id': self.id_, 'mpeg4_url': self.mpeg4_url}

        if self.mpeg4_width is not None:
            result['mpeg4_width'] = self.mpeg4_width
        if self.mpeg4_height is not None:
            result['mpeg4_height'] = self.mpeg4_height
        if self.thumb_url is not None:
            result['thumb_url'] = self.thumb_url
        if self.title is not None:
            result['title'] = self.title
        if self.caption is not None:
            result['caption'] = self.caption
        if self.message_text is not None:
            result['message_text'] = self.message_text
        if self.parse_mode is not None:
            result['parse_mode'] = self.parse_mode
        if self.disable_web_page_preview is not None:
            result['disable_web_page_preview'] = self.disable_web_page_preview
        return result


if __name__ == '__main__':
    obj = TelegramInlineQueryResultMPEG4GIF.gen_from_json_str(
        '{"id": "123213", "mpeg4_url": "ya.com", "title":"this is title", "message_text": "THIS IS message_text"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.id_
    print obj.title
    print obj.message_text
    print obj.mpeg4_url
    print obj.disable_web_page_preview
