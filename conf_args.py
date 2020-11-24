import logging
from exceptions import ConfigurationException
from conf import Configuration
import argparse

logger = logging.getLogger(__name__)


class ConfigurationArgs(Configuration):
    def __init__(self):
        self._parser = self._build_parser()
        super(ConfigurationArgs, self).__init__()
        self._set_arg_strings()

    def _set_arg_strings(self, args=None):
        if args == None:
            args = self._parser.parse_args()
        for arg in args.config:
            try:
                key, sep, value = arg.partition('=')
                if sep != '':
                    self[key] = value
            except Exception as e:
                pass

    @staticmethod
    def _build_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', metavar='key.path.string=value', type=str, nargs='*', help='configuration parameter')
        return parser
        