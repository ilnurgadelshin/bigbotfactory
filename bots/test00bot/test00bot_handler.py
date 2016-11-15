from bots.bot_handler import BotHandler
from bots.bot_command import TelegramBotCommand


class TestBotHandler(BotHandler):
    @TelegramBotCommand('off', short_description='unsubscribe', stop_after=False)
    def _off_subscription(self):
        self.add_output_text("You are unsubscribed from this bot. Use /on to subscribe."
                             "\nCreate your own bot: @bbfbot")
        self.add_output_text("You are unsubscribed from this bot again. Use /on to subscribe."
                             "\nCreate your own bot: @bbfbot")

    @TelegramBotCommand('about', short_description='show about')
    def _show_about(self):
        self.show_about()

    @TelegramBotCommand('set_about', short_description='set show about')
    def _set_about(self):
        self.set_about(self.update.message.text)

    def _process(self):
        text = self.update.message.text
        if text is None:
            text = 'None text!'
        self.add_output_text(text=text)
