from bots.bot_handler import BotHandler

from lib.dfa.dfa import DFA, DFAWaiter
from bots.telegram_dfa import TelegramDFA, TelegramDFAGoToInitialDFAException


class DFABotHandler(BotHandler):
    def _initial_dfa(self):
        raise NotImplementedError

    def _on_first_time_visit(self):
        pass

    def _process(self):
        dfa = None
        try:
            dumped_obj = self.bot_user_context.get_value('dumped_dfa')
            if dumped_obj is not None:
                dfa = DFAWaiter.deserialize(dumped_obj, {'chat_id': self.chat_id, 'bot_handler': self})
            else:
                self._on_first_time_visit()
        except:
            dfa = None
            # raise  # used for testing only!
        if dfa is None:
            dfa = self._initial_dfa()

        waiter = None
        while not isinstance(waiter, DFAWaiter):
            assert isinstance(dfa, DFA)
            wrapper_dfa = TelegramDFA(self.chat_id, self, dfa)
            try:
                waiter = wrapper_dfa.process(self.update)
                break
            except TelegramDFAGoToInitialDFAException:
                self.bot_user_context.clear_state()
                self.update = dfa._fix_update_on_change(self.update)
                dfa = self._initial_dfa()
        self.bot_user_context.set_value('dumped_dfa', waiter.serialize())
