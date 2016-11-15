# -*- coding: utf-8 -*-

from telegram.objects.inline_query_result import TelegramInlineQueryResult


class TelegramInlineQueryResultPhoto(TelegramInlineQueryResult):
    def __init__(self, id_, photo_url, photo_width=None, photo_height=None, thumb_url=None, title=None,
                 description=None, caption=None, message_text=None, parse_mode=None, disable_web_page_preview=False):
        assert id_ is not None
        assert photo_url is not None

        self.type = "photo"
        self.id_ = id_
        self.photo_url = photo_url
        self.photo_width = int(photo_width) if photo_width is not None else None
        self.photo_height = int(photo_height) if photo_height is not None else None
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.message_text = message_text
        assert parse_mode is None or parse_mode == "Markdown"
        self.parse_mode = parse_mode
        assert isinstance(disable_web_page_preview, bool)
        self.disable_web_page_preview = bool(disable_web_page_preview)

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramInlineQueryResultPhoto(
            id_=json_object['id'],
            photo_url=json_object['photo_url'],
            photo_width=json_object.get('photo_width'),
            photo_height=json_object.get('photo_height'),
            thumb_url=json_object.get('thumb_url'),
            title=json_object.get('title'),
            description=json_object.get('description'),
            caption=json_object.get('caption'),
            message_text=json_object.get('message_text'),
            parse_mode=json_object.get('parse_mode'),
            disable_web_page_preview=bool(json_object.get('disable_web_page_preview')),
        )

    def to_json(self):
        result = {'type': self.type, 'id': self.id_, 'photo_url': self.photo_url}

        if self.photo_width is not None:
            result['photo_width'] = self.photo_width
        if self.photo_height is not None:
            result['photo_height'] = self.photo_height
        if self.thumb_url is not None:
            result['thumb_url'] = self.thumb_url
        if self.title is not None:
            result['title'] = self.title
        if self.description is not None:
            result['description'] = self.description
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
    obj = TelegramInlineQueryResultPhoto.gen_from_json_str(
        '{"id": "123213", "photo_url": "ya.com", "title":"this is title", "message_text": "THIS IS message_text"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.id_
    print obj.title
    print obj.message_text
    print obj.photo_url
    print obj.disable_web_page_preview
