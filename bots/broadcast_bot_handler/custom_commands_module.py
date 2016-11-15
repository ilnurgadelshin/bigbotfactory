# -*- coding: utf-8 -*-

from bots.telegram_dfa import TelegramDFA
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands
from bots.generic_dfas.confirmation_dfa import TelegramDFAConfirm

from bots.broadcast_bot_handler.custom_commands_messages_module import CommandsMessagesDFA, AddMessageToCommandDFA
from bots.broadcast_bot_handler.custom_command_type import CustomCommandType
from bots.generic_dfas.go_to_root_dfa import TelegramDFAGoToRoot
import random
import time
import copy


class DeleteCustomCommandDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, cmd_id, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        self.bot_handler.remove_command(self.cmd_id)
        return self.exit_dfa


class NewCustomCommandDFA(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'

    COMMAND_MAX_LENGTH = 50

    def __init__(self, chat_id, bot_handler, parent_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler,
                                            default_message='Enter the name of the new command')
        self.exit_dfa = exit_dfa
        self.parent_id = parent_id
        self.set_command(self.CANCEL, exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'parent_id': self.parent_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['parent_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def process_input(self, update):
        text = update.message.text
        if text:
            new_command = text.strip()
            if len(new_command) > self.COMMAND_MAX_LENGTH:
                self.add_output_text("Sorry, bot command can't be longer than %d symbols" % self.COMMAND_MAX_LENGTH)
                return
            names = self.bot_handler.get_command_names(self.parent_id).values()
            if new_command in names:
                self.add_output_text("This command already exists")
                return
            cmd_id = self.bot_handler.create_command(new_command, self.parent_id)
            return AddMessageToCommandDFA(self.chat_id, self.bot_handler, cmd_id, self.exit_dfa)


class SetXYPlacementCustomCommandDFA(TelegramDFADefinedCommands):
    def __init__(self, chat_id, bot_handler, parent_id, x, y, new_cmd_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler,
                                            default_message='You can free this slot or assign a command:')
        self.exit_dfa = exit_dfa
        self.parent_id = parent_id
        self.new_cmd_id = new_cmd_id
        self.x = x
        self.y = y

    def _intern_dump(self, existing_ids):
        return {'parent_id': self.parent_id, 'x': self.x, 'y': self.y, 'new_cmd_id': self.new_cmd_id,
                'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['parent_id'],
            dumped_object['x'],
            dumped_object['y'],
            dumped_object['new_cmd_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def process_input(self, update):
        for cmd_id, cmd_name in self.bot_handler.get_command_names(self.parent_id).iteritems():
            x, y = self.bot_handler.get_command_xy(cmd_id)
            if x == self.x and y == self.y:
                self.bot_handler.set_command_xy(cmd_id, None, None)
        if self.new_cmd_id is not None:
            self.bot_handler.set_command_xy(self.new_cmd_id, self.x, self.y)
        return self.exit_dfa


class SelectXYPlacementCustomCommandDFA(TelegramDFADefinedCommands):
    FREE = 'Free this slot'
    BACK = u'⬅️'

    def __init__(self, chat_id, bot_handler, parent_id, x, y, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler,
                                            default_message='You can free this slot or assign a command:')
        self.exit_dfa = exit_dfa
        self.parent_id = parent_id
        self.x = x
        self.y = y

        self.set_command(
            self.FREE,
            SetXYPlacementCustomCommandDFA(self.chat_id, self.bot_handler, self.parent_id, x, y, None, exit_dfa))
        self.set_command(self.BACK, exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'parent_id': self.parent_id, 'x': self.x, 'y': self.y, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['parent_id'],
            dumped_object['x'],
            dumped_object['y'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        keyboard = [[self.FREE, self.BACK]]
        for cmd_id, cmd_name in self.bot_handler.get_command_names(self.parent_id).iteritems():
            self.set_command(
                cmd_name,
                SetXYPlacementCustomCommandDFA(self.chat_id, self.bot_handler, self.parent_id, self.x, self.y, cmd_id,
                                               self.exit_dfa))
            keyboard.append([cmd_name])
        self.set_keyboard(keyboard)


class PlacementCustomCommandDFA(TelegramDFADefinedCommands):
    BACK = u'⬅️'
    MAX_ROWS = 10
    MAX_COLS = 3

    def __init__(self, chat_id, bot_handler, parent_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa
        self.parent_id = parent_id
        self.set_command(self.BACK, exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'parent_id': self.parent_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['parent_id'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        xy_to_cmd_name = dict()
        not_used_cmds = []
        for cmd_id, cmd_name in self.bot_handler.get_command_names(self.parent_id).iteritems():
            x, y = self.bot_handler.get_command_xy(cmd_id)
            if x is not None and y is not None:
                if x not in xy_to_cmd_name:
                    xy_to_cmd_name[x] = dict()
                xy_to_cmd_name[x][y] = cmd_name
            else:
                not_used_cmds.append(cmd_name)
        self.set_message('Commands without a placement: ' + u', '.join(map(unicode, not_used_cmds)))

        for command in self.get_command_names():
            if isinstance(self.get_command_dfa(command), SelectXYPlacementCustomCommandDFA):
                self.remove_command(command)

        keyboard = []
        for x in xrange(self.MAX_ROWS):
            row = []
            for y in xrange(self.MAX_COLS):
                name = "[" + str(x) + ", " + str(y) + "]"
                if x in xy_to_cmd_name and y in xy_to_cmd_name[x]:
                    name = xy_to_cmd_name[x][y]
                row.append(name)
                self.set_command(
                    name,
                    SelectXYPlacementCustomCommandDFA(self.chat_id, self.bot_handler, self.parent_id, x, y, self))
            keyboard.append(row)
        keyboard.append([self.BACK])
        self.set_keyboard(keyboard)


class CustomCommandOutputDFA(TelegramDFADefinedCommands):
    BACK = u'⬅️'
    MAIN_MENU = u'⬆️'
    ATTRIBUTE_LAST_TIME_UPDATED = 'dfa_last_update_timestamp'

    def __init__(self, chat_id, bot_handler, cmd_id, preview_mode):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id
        self.preview_mode = preview_mode

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'preview_mode': self.preview_mode}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            dumped_object['preview_mode'],
        )

    @classmethod
    def upgrade_defined_dfa(cls, dfa_to_update, cmd_id):
        assert isinstance(dfa_to_update, TelegramDFADefinedCommands)
        keyboard = []
        xy_to_cmd_name = dict()
        for sub_cmd_id, sub_cmd in dfa_to_update.bot_handler.find_children(cmd_id).iteritems():
            x, y = sub_cmd['x'], sub_cmd['y']
            if x is not None and y is not None:
                if x not in xy_to_cmd_name:
                    xy_to_cmd_name[x] = dict()
                xy_to_cmd_name[x][y] = (sub_cmd_id, sub_cmd['command_name'])

        for x in sorted(xy_to_cmd_name.keys(), key=lambda value: value):
            row = []
            for y in sorted(xy_to_cmd_name[x].keys(), key=lambda value: value):
                dfa_to_update.set_command(
                    xy_to_cmd_name[x][y][1],
                    CustomCommandOutputDFA(
                        dfa_to_update.chat_id, dfa_to_update.bot_handler, xy_to_cmd_name[x][y][0], False))
                row.append(xy_to_cmd_name[x][y][1])
            if len(row):
                keyboard.append(row)
        return keyboard

    def update_menu(self, update):
        if self.preview_mode:
            return

        keyboard = CustomCommandOutputDFA.upgrade_defined_dfa(self, self.cmd_id)
        if len(keyboard):
            if not self.bot_handler.is_root(self.cmd_id):
                command = self.bot_handler.get_command(self.cmd_id)
                if not self.bot_handler.is_root(command['parent_id']):
                    self.set_command(self.BACK, CustomCommandOutputDFA(self.chat_id, self.bot_handler, command['parent_id'], False))
                else:
                    self.set_command(self.BACK, TelegramDFAGoToRoot(self.chat_id, self.bot_handler))
                keyboard.append([self.BACK])

                if not self.bot_handler.is_root(command['parent_id']):
                    self.set_command(self.MAIN_MENU, TelegramDFAGoToRoot(self.chat_id, self.bot_handler))
                    keyboard[-1].append(self.MAIN_MENU)
        self.set_keyboard(keyboard)

    def process_input(self, update):
        parent_id = None
        if not self.bot_handler.is_root(self.cmd_id):
            command = self.bot_handler.get_command(self.cmd_id)
            parent_id = command['parent_id']
            messages = command['messages']
            command_type = command['cmd_type']
            if command_type == CustomCommandType.ALL_MESSAGES:
                count = 0
                for message in messages:
                    count += 1
                    self.add_output_message(message)
                    if count >= 10:
                        break
            if command_type == CustomCommandType.RANDOM_MESSAGE and len(messages):
                self.add_output_message(random.choice(messages))

        if self.preview_mode:
            return CustomCommandViewDFA(self.chat_id, self.bot_handler, self.cmd_id)

        if not self.is_keyboard_empty():
            return None
        if not self.bot_handler.is_root(parent_id):
            return CustomCommandOutputDFA(self.chat_id, self.bot_handler, parent_id, False)
        else:
            return TelegramDFAGoToRoot(self.chat_id, self.bot_handler)


class RenameCustomCommandDFA(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'

    COMMAND_MAX_LENGTH = 50

    def __init__(self, chat_id, bot_handler, cmd_id, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler,
                                            default_message='Enter the name of the new command')
        self.exit_dfa = exit_dfa
        self.cmd_id = cmd_id
        self.parent_id = bot_handler.get_command_parent(cmd_id)
        self.set_command(self.CANCEL, exit_dfa)

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def process_input(self, update):
        text = update.message.text
        if text:
            new_command = text.strip()
            if len(new_command) > self.COMMAND_MAX_LENGTH:
                self.add_output_text("Sorry but a bot command cannot exceed %d symbols" % self.COMMAND_MAX_LENGTH)
                return
            names = self.bot_handler.get_command_names(self.parent_id).values()
            if new_command in names:
                self.add_output_text("This command already exists")
                return
            self.bot_handler.set_command_name(self.cmd_id, new_command)
            return self.exit_dfa


class CustomCommandViewDFA(TelegramDFADefinedCommands):
    VIEW = 'Preview'
    RENAME = 'Rename'
    MESSAGES = 'Messages'
    NEW_COMMAND = 'Add sub command'
    PLACEMENT = 'Placement'

    DELETE = 'Delete'
    BACK = u'⬅️'
    MAIN_MENU = u'⬆️'

    def __init__(self, chat_id, bot_handler, cmd_id):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.cmd_id = cmd_id

    def _intern_dump(self, existing_ids):
        return {'cmd_id': self.cmd_id}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['cmd_id'],
        )

    def update_menu(self, update):
        parent_id = None
        if not self.bot_handler.is_root(self.cmd_id):
            command = self.bot_handler.get_command(self.cmd_id)
            parent_id = command['parent_id']
            self.set_command(self.VIEW, CustomCommandOutputDFA(self.chat_id, self.bot_handler, self.cmd_id, True))
            self.set_command(self.RENAME, RenameCustomCommandDFA(self.chat_id, self.bot_handler, self.cmd_id, self))
            self.set_command(self.MESSAGES, CommandsMessagesDFA(self.chat_id, self.bot_handler, self.cmd_id, self))
            self.set_command(
                self.DELETE,
                TelegramDFAConfirm(
                    self.chat_id, self.bot_handler,
                    default_text="Are you sure you want to delete this command?",
                    confirm_dfa=DeleteCustomCommandDFA(
                        self.chat_id, self.bot_handler, self.cmd_id,
                        CustomCommandViewDFA(self.chat_id, self.bot_handler, command['parent_id'])),
                    no_dfa=self))

        keyboard = []
        for cmd_id, cmd_name in self.bot_handler.get_command_names(self.cmd_id).iteritems():
            cmd_name_text = cmd_name
            self.set_command(cmd_name_text, CustomCommandViewDFA(self.chat_id, self.bot_handler, cmd_id))
            keyboard.append([cmd_name_text])

        self.set_command(self.NEW_COMMAND, NewCustomCommandDFA(self.chat_id, self.bot_handler, self.cmd_id, self))
        self.set_command(self.PLACEMENT, PlacementCustomCommandDFA(self.chat_id, self.bot_handler, self.cmd_id, self))
        keyboard.append([self.NEW_COMMAND, self.PLACEMENT])
        keyboard += [[self.VIEW, self.RENAME, self.MESSAGES]]

        if self.bot_handler.is_root(self.cmd_id):
            self.set_command(self.BACK, TelegramDFAGoToRoot(self.chat_id, self.bot_handler))
            keyboard.append([self.BACK])
        else:
            self.set_command(self.BACK, CustomCommandViewDFA(self.chat_id, self.bot_handler, parent_id))
            if not self.bot_handler.is_root(parent_id):
                self.set_command(self.MAIN_MENU, CustomCommandViewDFA(self.chat_id, self.bot_handler, None))
                keyboard.append([self.DELETE, self.BACK, self.MAIN_MENU])
            else:
                keyboard.append([self.DELETE, self.BACK])
        self.set_keyboard(keyboard)

    def process_input(self, update):
        print 'cmd_id: ', self.cmd_id
        text = "Manage command: " + self.bot_handler.get_command_path(self.cmd_id)
        if not self.bot_handler.is_root(self.cmd_id) and self.bot_handler.get_command_xy(self.cmd_id)[0] is None:
            text += " (invisible, set the placement)"
        self.set_message(text)
