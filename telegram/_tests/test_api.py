# -*- coding: utf-8 -*-

# to run the test you need to use your bot's token and your chat_id and start a chat session

import filecmp

from telegram.objects.input_file import TelegramInputFile
from telegram.api.core.api import TelegramAPIHandler
from telegram.objects.reply_keyboard_markup import TelegramReplyKeyBoardMarkup


def main():
    token = '##########'
    chat_id = 999999

    handler = TelegramAPIHandler(token)
    user = handler.get_me()
    print "Myself: ", user.to_json_str()
    assert user is not None, "You have to start a chat with this bot"

    print "Sending a message with keyboard"
    keyboard = TelegramReplyKeyBoardMarkup(keyboard=[[u'привет❤️ uni!', 'привет❤️! utf8']])
    print keyboard.to_json_str()
    response = handler.send_message(chat_id=chat_id, text=u'привет❤️!', reply_markup=keyboard)
    assert response.result is not None

    print "Sending a simple message"
    response = handler.send_message(chat_id=chat_id, text=u'привет❤️!')
    assert response.result is not None

    print "Sending some location"
    response = handler.send_location(chat_id=chat_id, latitude=55.725033, longitude=37.580149)
    assert response.result is not None

    print "Getting user's profile pictures"
    user_profile_photos = handler.get_user_profile_photos(user_id=chat_id)
    assert user_profile_photos is not None

    print "Sending an action....", handler.send_chat_action(chat_id=chat_id, action='typing')

    print "sending a photo"
    input_photo = TelegramInputFile('resources/09042010.jpg')
    message = handler.send_photo(chat_id=chat_id, photo=input_photo, caption='input photo')
    assert message is not None
    for p in message.photo:
        print "Generated file_id: ", p.file_id

    print "sending photo by id"
    message = handler.send_photo(chat_id=chat_id, photo=message.photo[0].file_id, caption='input photo by id')
    assert message is not None
    print "Used file_id: ", message.photo[0].file_id

    print "sending a voice file"
    input_voice = TelegramInputFile('resources/fallbackring.ogg')
    message = handler.send_voice(chat_id=chat_id, voice=input_voice, duration=3)
    assert message is not None
    print "Generated file_id: ", message.voice.file_id

    print "sending an audio file"
    input_audio = TelegramInputFile('resources/test_cbr.mp3')
    message = handler.send_audio(chat_id=chat_id, audio=input_audio, duration=3)
    assert message is not None
    print "Generated file_id: ", message.audio.file_id

    print "Downloading file back and comparing"
    handler.get_file(message.audio.file_id, 'resources/test_cbr_download.mp3')
    assert filecmp.cmp('resources/test_cbr.mp3', 'resources/test_cbr_download.mp3'), "Files are not equal"

    # next line is not working, not sure why, but response doesn't contain audio.file_id
    # print "Generated file_id: ", message.audio.file_id
    # need to add a send-by-id test here after id will be available

    print "sending a document 1"
    input_doc1 = TelegramInputFile('resources/p1.pdf')
    message = handler.send_document(chat_id=chat_id, document=input_doc1)
    assert message is not None
    print "Generated file_id: ", message.document.file_id

    print "sending document 1 by id"
    message = handler.send_document(chat_id=chat_id, document=message.document.file_id)
    assert message is not None
    print "Used file_id: ", message.document.file_id

    print "sending a document 2"
    input_doc2 = TelegramInputFile('resources/test_cbr.mp3')
    message = handler.send_document(chat_id=chat_id, document=input_doc2)
    assert message is not None
    print message.to_json_str()
    # next line is not working, probably the same reason
    # print "Generated file_id: ", message.document.file_id
    # need to add a send-by-id test here after id will be available

    print "sending a sticker"
    input_sticker = TelegramInputFile('resources/test_sticker.webp')
    message = handler.send_sticker(chat_id=chat_id, sticker=input_sticker)
    assert message is not None
    print "Generated file_id: ", message.sticker.file_id

    print "sending a sticker by id"
    message = handler.send_sticker(chat_id=chat_id, sticker=message.sticker.file_id)
    assert message is not None
    print "Used file_id: ", message.sticker.file_id

    print "sending a mp4 video"
    input_video = TelegramInputFile('resources/videoviewdemo.mp4')
    message = handler.send_video(chat_id=chat_id, video=input_video)
    assert message is not None
    print "Generated file_id: ", message.video.file_id

    print "sending a mp4 video by id"
    message = handler.send_video(chat_id=chat_id, video=message.video.file_id)
    assert message is not None
    print "Used file_id: ", message.video.file_id

    print "sending a video as a document"
    input_video2 = TelegramInputFile('resources/09112007.3gp')
    message = handler.send_document(chat_id=chat_id, document=input_video2)
    assert message is not None
    print "Generated file_id: ", message.document.file_id

    print "sending a video as a document by id"
    message = handler.send_document(chat_id=chat_id, document=message.document.file_id)
    assert message is not None
    print "Used file_id: ", message.document.file_id

    print "Sending a message with keyboard"
    keyboard = TelegramReplyKeyBoardMarkup(keyboard=[[u'привет❤️ uni!', 'привет❤️! utf8']])
    print keyboard.to_json_str()
    response = handler.send_message(chat_id=chat_id, text=u'привет❤️!', reply_markup=keyboard)
    assert response.result is not None



if __name__ == '__main__':
    main()
