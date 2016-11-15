

# if you wish to add a special handler function for some particular command
# just create a function and decorate it with this class object
class TelegramBotCommand(object):
    def __init__(self, cmd_name, admin_only=False, short_description=None, stop_after=True):
        self.cmd_name = cmd_name
        self.admin_only = admin_only
        self.short_description = short_description
        self.stop_after = stop_after

    def __call__(self, original_func):
        original_func.telegram_bot_command = self.cmd_name
        original_func.admin_only = self.admin_only
        original_func.short_description = self.short_description
        original_func.stop_after = self.stop_after
        return original_func
