# -*- coding: utf-8 -*-

from telegram.objects.inline_query_result import TelegramInlineQueryResult


class TelegramInlineQueryResultVideo(TelegramInlineQueryResult):
    def __init__(self, id_, video_url, mime_type, message_text, parse_mode=None, disable_web_page_preview=False,
                 video_width=None, video_height=None, video_duration=None, thumb_url=None, title=None,
                 description=None):
        assert id_ is not None
        assert video_url is not None
        assert mime_type == "text/html" or mime_type == "video/mp4"
        assert message_text is not None

        self.type = "mpeg4_gif"
        self.id_ = id_
        self.video_url = video_url
        self.mime_type = mime_type
        self.message_text = message_text
        assert parse_mode is None or parse_mode == "Markdown"
        self.parse_mode = parse_mode
        assert isinstance(disable_web_page_preview, bool)
        self.disable_web_page_preview = bool(disable_web_page_preview)
        self.video_width = int(video_width) if video_width is not None else None
        self.video_height = int(video_height) if video_height is not None else None
        self.video_duration = int(video_duration) if video_duration is not None else None
        self.thumb_url = thumb_url
        self.title = title
        self.description = description

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramInlineQueryResultVideo(
            id_=json_object['id'],
            video_url=json_object['video_url'],
            mime_type=json_object['mime_type'],
            message_text=json_object['message_text'],
            parse_mode=json_object.get('parse_mode'),
            disable_web_page_preview=bool(json_object.get('disable_web_page_preview')),
            video_width=json_object.get('video_width'),
            video_height=json_object.get('video_height'),
            video_duration=json_object.get('video_duration'),
            thumb_url=json_object.get('thumb_url'),
            title=json_object.get('title'),
            description=json_object.get('description'),
        )

    def to_json(self):
        result = {'type': self.type, 'id': self.id_, 'video_url': self.video_url, 'mime_type': self.mime_type,
                  'message_text': self.message_text}

        if self.parse_mode is not None:
            result['parse_mode'] = self.parse_mode
        if self.disable_web_page_preview is not None:
            result['disable_web_page_preview'] = self.disable_web_page_preview
        if self.video_width is not None:
            result['video_width'] = self.video_width
        if self.video_height is not None:
            result['video_height'] = self.video_height
        if self.video_duration is not None:
            result['video_duration'] = self.video_duration
        if self.thumb_url is not None:
            result['thumb_url'] = self.thumb_url
        if self.title is not None:
            result['title'] = self.title
        if self.description is not None:
            result['description'] = self.description
        return result


if __name__ == '__main__':
    obj = TelegramInlineQueryResultVideo.gen_from_json_str(
        '{"id": "123213", "video_url": "ya.com", "mime_type": "text/html", "title":"this is title", "message_text": "THIS IS message_text"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.id_
    print obj.title
    print obj.message_text
    print obj.video_url
    print obj.mime_type
    print obj.disable_web_page_preview
