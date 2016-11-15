import random
import simplejson as json
import zlib
import base64


class DFAWaiter(object):
    def __init__(self, dfa):
        self.dfa = dfa
        assert isinstance(self.dfa, DFA)

    def serialize(self):
        return json.dumps(self.dfa.dump(set()))
        # return base64.b64encode(zlib.compress(json.dumps(self.dfa.dump(set())), 9))

    @classmethod
    def deserialize(cls, serialized_object, context):
        # dumped_obj = json.loads(zlib.decompress(base64.b64decode(serialized_object)))
        dumped_obj = json.loads(serialized_object)
        context['__existing_ids'] = {}
        return DFA.load(dumped_obj, context)


class DFALoadingWaiter(object): pass


class DFA(object):  # Deterministic Finite Automaton
    def __init__(self, start_dfa=None):
        self.id = None
        self.start_dfa = start_dfa
        self.current_dfa = None
        self._change_dfa(self.start_dfa)

    def generate_id(self):
        if self.id is None:
            self.id = random.randint(1000, 1000000000)
        return self.id

    def clear_id(self):
        self.id = None

    def set_id(self, new_id):
        self.id = new_id
        return self

    def _fix_update_on_change(self, update):
        return update

    def _change_dfa(self, dfa_name):
        self.current_dfa = dfa_name

    def assert_update(self, update):
        # each DFA accepts updates from a fixed Alphabet only, so you must add some assertion here
        raise NotImplementedError

    def wait(self):
        return DFAWaiter(self)

    def dump(self, existing_ids):  # final method
        if self.id is not None:
            # this dfa has already been dumped
            return self.id, None, None, None
        while True:
            self.generate_id()
            if self.id not in existing_ids:
                existing_ids.add(self.id)  # the order is important here, MUST call before _dump
                break
            self.clear_id()
        return self.id, self.__class__.__module__, self.__class__.__name__, self._intern_dump(existing_ids)

    def _intern_dump(self, existing_ids):
        return {}

    @classmethod
    def load(cls, dumped_object, context):
        dump_result_id, module_name, class_name, dump_result = dumped_object
        if dump_result_id not in context['__existing_ids']:
            context['__existing_ids'][dump_result_id] = DFALoadingWaiter()
        if dump_result is None:
            return context['__existing_ids'][dump_result_id]
        dfa_class = getattr(__import__(module_name, fromlist=[class_name]), class_name)
        assert issubclass(dfa_class, DFA)
        loaded_dfa = dfa_class._intern_load(dump_result, context)
        if isinstance(loaded_dfa, DFA):
            context['__existing_ids'][dump_result_id] = loaded_dfa
        return loaded_dfa

    @classmethod
    def _intern_load(cls, dumped_object, context):
        raise NotImplementedError

    def process(self, update):
        self.assert_update(update)
        while self.current_dfa is not None:
            dfa_result = self.current_dfa.process(update)
            if dfa_result is None:
                waiter = self.current_dfa.wait()
                return waiter
            if isinstance(dfa_result, DFAWaiter):
                return dfa_result
            assert isinstance(dfa_result, DFA)
            self._change_dfa(dfa_result)
            update = self._fix_update_on_change(update)
        self._change_dfa(self.start_dfa)
        t = self.on_terminate(update)
        return t

    def on_terminate(self, update):
        print "Warning! Not implemented function"
