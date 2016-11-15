# -*- coding: utf-8 -*-


class BotHandlerUtils(object):
    @classmethod
    def get_rate_us_message(cls, bot_user):
        return u"\n ⭐️⭐️⭐️⭐️⭐️ Rate us https://telegram.me/storebot?start=" + bot_user.username

    @classmethod
    def get_contact_us_message(cls):
        return "\nCreate your own bot: @bbfbot"