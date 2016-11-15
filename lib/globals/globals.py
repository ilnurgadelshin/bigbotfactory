class GlobalParams(object):
    API_VERSION_PARAM = 'API_VERSION_PARAM'

    @classmethod
    def is_param_name(cls, name):
        return name.endswith('_PARAM')

    @classmethod
    def get_all_params(cls):
        result = []
        for attr_name in dir(cls):
            if cls.is_param_name(attr_name):
                result.append(attr_name)
        return result


class Globals(object):
    """
    This is a pure coding anti-pattern. Please, consider using it super rarely as it can lead to non-debugable mess
    in your code. Right now it's used for storing some lambda context variables as API version.

    Implements singletone, so change a value somewhere will affect all other places!
    """

    @classmethod
    def set(cls, key, value):
        assert GlobalParams.is_param_name(key)
        setattr(cls, key, value)

    @classmethod
    def get(cls, key):
        assert hasattr(cls, key), 'Globals must have a key when requested'
        return getattr(cls, key)

    @classmethod
    def initialize_from_args(cls, args):
        for attr_params in GlobalParams.get_all_params():
            cls.set(attr_params, args[attr_params])

    @classmethod
    def dump_to_args(cls):
        result = {}
        for attr_params in GlobalParams.get_all_params():
            result[attr_params] = cls.get(attr_params)
        return result

