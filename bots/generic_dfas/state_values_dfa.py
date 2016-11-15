from bots.telegram_dfa import TelegramDFA


class TelegramDFASetStateValue(TelegramDFA):
    def __init__(self, chat_id, bot_handler, key, value, exit_dfa):
        TelegramDFA.__init__(self, chat_id=chat_id, bot_handler=bot_handler)
        self.key = key
        self.value = value
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'key': self.key, 'value': self.value, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, loader):
        return cls(
            loader.context['chat_id'],
            loader.context['bot_handler'],
            dumped_object['key'],
            dumped_object['value'],
            loader.load(dumped_object['exit_dfa']),
        )

    def on_terminate(self, update):
        self.bot_handler.bot_user_context.set_value(self.key, self.value)
        return self.exit_dfa


class TelegramDFAStateAddValueToSet(TelegramDFA):
    def __init__(self, chat_id, bot_handler, set_variable_name, value, exit_dfa):
        TelegramDFA.__init__(self, chat_id=chat_id, bot_handler=bot_handler)
        self.set_variable_name = set_variable_name
        self.value = value
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'key': self.set_variable_name, 'value': self.value, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['key'],
            dumped_object['value'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        value = self.bot_handler.bot_user_context.get_value(self.set_variable_name)
        if value is None:
            self.bot_handler.bot_user_context.set_value(self.set_variable_name, list([self.value]))
        else:
            assert isinstance(value, list)
            if self.value not in value:
                value.append(self.value)
                self.bot_handler.bot_user_context.set_value(self.set_variable_name, value)
        return self.exit_dfa


class TelegramDFAStateRemoveValueFromSet(TelegramDFA):
    def __init__(self, chat_id, bot_handler, set_variable_name, value, exit_dfa):
        TelegramDFA.__init__(self, chat_id=chat_id, bot_handler=bot_handler)
        self.set_variable_name = set_variable_name
        self.value = value
        self.exit_dfa = exit_dfa

    def _intern_dump(self, existing_ids):
        return {'key': self.set_variable_name, 'value': self.value, 'exit_dfa': self.exit_dfa.dump(existing_ids)}

    @classmethod
    def _intern_load(cls, dumped_object, context):
        return cls(
            context['chat_id'],
            context['bot_handler'],
            dumped_object['key'],
            dumped_object['value'],
            cls.load(dumped_object['exit_dfa'], context),
        )

    def on_terminate(self, update):
        value = self.bot_handler.bot_user_context.get_value(self.set_variable_name)
        if value is not None and isinstance(value, list) and self.value in value:
            value.remove(self.value)
            self.bot_handler.bot_user_context.set_value(self.set_variable_name, value)
        return self.exit_dfa