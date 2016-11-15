class BotsFactory(object):
    # DON'T CHANGE CONSTANTS BELOW! Bots' webhook urls are using these value!
    TEST00BOT = "TEST00BOT"
    BROADCAST_BOT = "BROADCAST_BOT"
    BBF_BOT = "BBF_BOT"

    @classmethod
    def get_by_name(cls, bot_name=None):
        bot_handler = None
        if bot_name == BotsFactory.TEST00BOT:
            from bots.test00bot.test00bot_handler import TestBotHandler
            bot_handler = TestBotHandler
        if bot_name == BotsFactory.BROADCAST_BOT:
            from bots.broadcast_bot_handler.broadcast_bot_handler import BroadcastBotHandler
            bot_handler = BroadcastBotHandler
        if bot_name == BotsFactory.BBF_BOT:
            from bots.bbfbot.bbfbot_handler import BBFHandler
            bot_handler = BBFHandler
        return bot_handler

if __name__ == '__main__':
    handler = BotsFactory.get_by_name('TEST00BOT')
    print handler.__class__



