import ConfigParser


class ConfigReader(object):
    def __init__(self, filename):
        self._config = ConfigParser.RawConfigParser()
        self._config.read(filename)

    def read_option(self, section, option):
        try:
            return self._config.get(section, option)
        except:
            return None

    def read_list_option(self, section, option):
        return [item.strip() for item in self.read_option(section, option).split(',')]
