# -*- coding: utf-8 -*-
from bots.generic_dfas.defined_commands import TelegramDFADefinedCommands

from bots.telegram_dfa import TelegramDFA
from bots.libs.entities.bot_subscribers import BotSubscribers
from bots.generic_dfas.state_values_dfa import TelegramDFAStateAddValueToSet, TelegramDFAStateRemoveValueFromSet
from bots.dfa_modules.channels_module import AddChannelsDFA


STATE_MESSAGES = 'new_post_messages'
STATE_PUBLISH_TO = 'new_post_publish_to'
SUBSCRIBERS_NAME = 'Subscribers'


class SendMessagesToDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, chat_ids, clear_messages, exit_dfa, async=True, channels=None):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa
        self.chat_ids = chat_ids
        self.clear_messages = clear_messages
        self.async = async
        self.channels = channels

    def _intern_dump(self, existing_ids):
        return {'chat_ids': self.chat_ids,
                'clear_messages': self.clear_messages,
                'exit_dfa': self.exit_dfa.dump(existing_ids),
                'async': self.async,
                'channels': self.channels}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['chat_ids'],
            dumped_object['clear_messages'],
            cls.load(dumped_object['exit_dfa'], context),
            dumped_object['async'],
            dumped_object['channels'],
        )

    def on_terminate(self, update):
        messages = self.bot_handler.bot_user_context.get_value(STATE_MESSAGES, [])
        if self.channels is not None:
            channels_to_send = []
            for channel in self.channels:
                if channel.startswith('@'):
                    channels_to_send.append(channel)
                else:
                    channels_to_send.append('@' + channel)
            self.bot_handler.api_handler.send_telegram_messages(channels_to_send, messages, async=self.async)
        self.bot_handler.api_handler.send_telegram_messages(
            self.chat_ids, messages, async=self.async,
            send_stats_to_chat_ids=[self.chat_id] if self.async else None)
        if self.clear_messages:
            self.bot_handler.bot_user_context.set_value(STATE_MESSAGES, [])
            self.bot_handler.bot_user_context.set_value(STATE_PUBLISH_TO, [SUBSCRIBERS_NAME])
        return self.exit_dfa


class PublishPostDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        channels = self.bot_handler.bot_user_context.get_value(STATE_PUBLISH_TO, [])[::]
        chat_ids = []
        text = "Done. Your post has been sent"
        if SUBSCRIBERS_NAME in channels:
            chat_ids = BotSubscribers(self.bot_handler.api_handler.get_bot_id()).get_all_subscribers()
            channels.remove(SUBSCRIBERS_NAME)
            self.bot_handler.bot_user_context.set_value(SUBSCRIBERS_NAME, channels)
            text += " to %d subscribers" % len(chat_ids)
        if len(channels):
            text += " to %d channels" % len(channels)
        self.add_output_text(text)
        return SendMessagesToDFA(
            self.chat_id, self.bot_handler, chat_ids, True, self.exit_dfa, async=True, channels=channels)


class PreviewPostDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        return SendMessagesToDFA(self.chat_id, self.bot_handler, [self.chat_id], False, self.exit_dfa, async=False)


class RemoveLastMessageFromStateDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        messages = self.bot_handler.bot_user_context.get_value(STATE_MESSAGES, [])[::]
        if len(messages):
            messages.pop()
            self.bot_handler.bot_user_context.set_value(STATE_MESSAGES, messages)
        return self.exit_dfa


class RemoveAllMessagesFromStateDFA(TelegramDFA):
    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFA.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def on_terminate(self, update):
        self.bot_handler.bot_user_context.set_value(STATE_MESSAGES, [])
        return self.exit_dfa


class NewPostDFA(TelegramDFADefinedCommands):
    CANCEL = 'Cancel'
    PUBLISH = 'Publish'
    PREVIEW = 'Preview'
    REMOVE_LAST = 'Remove Last'
    REMOVE_ALL = 'Remove All'
    ADD_CHANNEL = 'Add a channel'

    SELECTED_ICON = u'✅'
    MAX_POSTS = 10

    def __init__(self, chat_id, bot_handler, exit_dfa):
        TelegramDFADefinedCommands.__init__(self, chat_id, bot_handler)
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            cls.load(dumped_object['exit_dfa'], context)
        )

    def update_menu(self, update):
        self.set_command(self.CANCEL, self.exit_dfa)
        self.set_command(self.PREVIEW, PreviewPostDFA(self.chat_id, self.bot_handler, self))
        self.set_command(self.PUBLISH, PublishPostDFA(self.chat_id, self.bot_handler, self.exit_dfa))
        self.set_command(self.REMOVE_LAST, RemoveLastMessageFromStateDFA(self.chat_id, self.bot_handler, self))
        self.set_command(self.REMOVE_ALL, RemoveAllMessagesFromStateDFA(self.chat_id, self.bot_handler, self))
        self.set_command(self.ADD_CHANNEL, AddChannelsDFA(self.chat_id, self.bot_handler, self))

        if STATE_PUBLISH_TO not in self.bot_handler.bot_user_context:
            self.bot_handler.bot_user_context.set_value(STATE_PUBLISH_TO, [SUBSCRIBERS_NAME])
        if STATE_MESSAGES not in self.bot_handler.bot_user_context:
            self.bot_handler.bot_user_context.set_value(STATE_MESSAGES, [])

        messages = self.bot_handler.bot_user_context.get_value(STATE_MESSAGES, [])[::]
        print messages
        current_messages_count = len(messages)

        self.set_enable(self.REMOVE_LAST, current_messages_count > 0)
        self.set_enable(self.REMOVE_ALL, current_messages_count > 0)
        keyboard = [[self.PREVIEW, self.PUBLISH], ]
        if current_messages_count:
            keyboard.append([self.REMOVE_LAST, self.REMOVE_ALL])
        keyboard.append([self.ADD_CHANNEL])

        values_to_check = [SUBSCRIBERS_NAME] + list(self.bot_handler.get_channels())
        for value in values_to_check:
            print self.bot_handler.bot_user_context.get_value(STATE_PUBLISH_TO, [])
            if value in self.bot_handler.bot_user_context.get_value(STATE_PUBLISH_TO, []):
                self.remove_command(value)
                self.set_command(
                    self.SELECTED_ICON + value,
                    TelegramDFAStateRemoveValueFromSet(self.chat_id, self.bot_handler, STATE_PUBLISH_TO, value, self))
                keyboard.append([self.SELECTED_ICON + value])
            else:
                self.remove_command(self.SELECTED_ICON + value)
                self.set_command(
                    value,
                    TelegramDFAStateAddValueToSet(self.chat_id, self.bot_handler, STATE_PUBLISH_TO, value, self))
                keyboard.append([value])

        keyboard.append([self.CANCEL])
        self.set_keyboard(keyboard)

    def process_input(self, update):
        messages = self.bot_handler.bot_user_context.get_value(STATE_MESSAGES, [])[::]
        current_messages_count = len(messages)

        message = "Add a new message or Preview/Publish\n"
        if current_messages_count >= self.MAX_POSTS:
            message = "You cannot add more messages to this string. Please publish or edit the existing messages.\n"
        else:
            if update.message.has_non_empty_content():
                messages.append(update.message.to_json_str())
                self.bot_handler.bot_user_context.set_value(STATE_MESSAGES, messages)
                current_messages_count += 1
        message += "Messages in the stack: %d\n" % current_messages_count
        if len(self.bot_handler.bot_user_context.get_value(STATE_PUBLISH_TO, [])):
            message += "Will be sent to: " + ", ".join(self.bot_handler.bot_user_context.get_value(STATE_PUBLISH_TO))
        else:
            message += "Please, select who will receive the post"
        self.set_message(message)
