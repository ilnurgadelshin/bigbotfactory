from telegram_utils.string import to_utf8
from bots.telegram_dfa import TelegramDFA

from telegram.objects.reply_keyboard_markup import TelegramReplyKeyBoardMarkup


class TelegramDFADefinedCommands(TelegramDFA):
    def __init__(self, chat_id, bot_handler, default_message='', keyboard=None):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.commands = dict()  # command => {'enabled' => bool, 'short_description' => text, 'dfa' => TelegramDFA}
        self.default_message = ''
        self.set_message(default_message)

        self.keyboard = None
        self.set_keyboard(keyboard)

    def _intern_dump(self, existing_ids):
        r = {
            'default_message': self.default_message,
            'keyboard': None
        }
        if self.keyboard is not None:
            for command_name, command in self.commands.iteritems():
                r['keyboard'][command_name] = {
                    'enabled': command['enabled'],
                    'short_description': command['short_description'],
                    'dfa': command['dfa'].dump(existing_ids),
                    }
        return r


    @classmethod
    def _intern_load(cls, dumped_object, context):
        dumped_keyboard = dumped_object['keyboard']
        keyboard = None
        if dumped_keyboard is not None:
            keyboard = {}
            for command_name, dumped_command in dumped_keyboard.iteritems():
                keyboard[command_name] = {
                    'enabled': dumped_command['enabled'],
                    'short_description': dumped_command['short_description'],
                    'dfa': cls.load(dumped_command['dfa'], context),
                }
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['default_message'],
            keyboard,
        )

    def has_command(self, command):
        return command in self.commands

    def get_command_names(self):
        return self.commands.keys()

    def set_command(self, command, end_dfa, enabled=True, short_description=None):
        self.commands[command] = {
            'enabled': enabled,
            'short_description': short_description,
            'dfa': end_dfa,
        }
        return self

    def set_enable(self, command, enabled):
        assert command in self.commands, '%s is not in commands' % command
        self.commands[command]['enabled'] = bool(enabled)

    def is_enabled(self, command):
        assert command in self.commands
        return bool(self.commands[command]['enabled'])

    def get_command_dfa(self, command):
        assert command in self.commands
        return self.commands[command]['dfa']

    def set_short_description(self, command, short_description):
        assert command in self.commands
        self.commands[command]['short_description'] = short_description

    def remove_command(self, command):
        if command in self.commands:
            self.commands.pop(command)
        return self

    def set_message(self, message):
        self.default_message = message.strip()

    def set_keyboard(self, keyboard):
        self.keyboard = keyboard  # All commands in the format: [['cmd1', 'cmd2'], ['cmd3']].

    def is_keyboard_empty(self):
        return len(self.keyboard) == 0

    @staticmethod
    def get_canonical_string(string, is_list_view):
        if not is_list_view:
            return string
        return '/' + to_utf8(string.replace(' ', '_')).replace('@', '').replace('\\', '')

    def process_input(self, update):
        pass

    def update_menu(self, update):
        pass

    def on_terminate(self, update):
        self.update_menu(update)
        text = update.message.text
        # running this before process_input is error-prone: constructor may not create all commands on the keyboard.
        # as a results, we won't be able to hit any button set or added in process_input
        if text is not None:
            for command_name, command in self.commands.iteritems():
                if not command['enabled']:
                    continue
                expecting_command = TelegramDFADefinedCommands.get_canonical_string(command_name, None)
                if to_utf8(text) == to_utf8(expecting_command):
                    return command['dfa']

        dfa_result = self.process_input(update)
        if dfa_result is not None:
            return dfa_result

        text = self.default_message
        selective = None
        if self.chat_id < 0 and update.message.from_.username is not None:
            text += "\n @" + update.message.from_.username
            selective = True
        if text:
            self.add_output_text(text)

        keyboard = []
        for command_name, command in self.commands.iteritems():
            if not command['enabled']:
                continue
            keyboard.append([command_name])
        if self.keyboard is not None:
            keyboard = self.keyboard
        reply = None
        if len(keyboard):
            reply = TelegramReplyKeyBoardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False,
                                                selective=selective)
        self.set_output_reply(reply)
