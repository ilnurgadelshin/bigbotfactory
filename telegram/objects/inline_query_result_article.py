# -*- coding: utf-8 -*-

from telegram.objects.inline_query_result import TelegramInlineQueryResult


class TelegramInlineQueryResultArticle(TelegramInlineQueryResult):
    def __init__(self, id_, title, message_text, parse_mode=None, disable_web_page_preview=False,
                 url=None, hide_url=False, description=None, thumb_url=None, thumb_width=None, thumb_height=None):
        assert id_ is not None
        assert title is not None
        assert message_text is not None

        self.type = "article"
        self.id_ = id_
        self.title = title
        self.message_text = message_text
        assert parse_mode is None or parse_mode == "Markdown"
        self.parse_mode = parse_mode

        assert isinstance(disable_web_page_preview, bool)
        self.disable_web_page_preview = bool(disable_web_page_preview)
        self.url = url
        assert isinstance(hide_url, bool)
        self.hide_url = hide_url

        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = int(thumb_width) if thumb_width is not None else None
        self.thumb_height = int(thumb_height) if thumb_width is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramInlineQueryResultArticle(
            id_=json_object['id'],
            title=json_object['title'],
            message_text=json_object['message_text'],
            parse_mode=json_object.get('parse_mode'),
            disable_web_page_preview=bool(json_object.get('disable_web_page_preview')),
            url=json_object.get('url'),
            hide_url=bool(json_object.get('hide_url')),
            description=json_object.get('description'),
            thumb_url=json_object.get('thumb_url'),
            thumb_width=json_object.get('thumb_width'),
            thumb_height=json_object.get('thumb_height'),
        )

    def to_json(self):
        result = {'type': self.type, 'id': self.id_, 'title': self.title, 'message_text': self.message_text,
                  'disable_web_page_preview': self.disable_web_page_preview, 'hide_url': self.hide_url}
        if self.parse_mode is not None:
            result['parse_mode'] = self.parse_mode
        if self.url is not None:
            result['url'] = self.url
        if self.description is not None:
            result['description'] = self.description
        if self.thumb_url is not None:
            result['thumb_url'] = self.thumb_url
        if self.thumb_width is not None:
            result['thumb_width'] = self.thumb_width
        if self.thumb_height is not None:
            result['thumb_height'] = self.thumb_height
        return result


if __name__ == '__main__':
    obj = TelegramInlineQueryResultArticle.gen_from_json_str(
        '{"id": "123213", "title":"this is title", "message_text": "THIS IS message_text", "url": "ya.com"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.id_
    print obj.title
    print obj.message_text
    print obj.url
    print obj.disable_web_page_preview
    print obj.hide_url
