import logging
import operator
from functools import reduce
from functools import partial
from exceptions import ConfigurationException
from conf import Configuration
import os
import re
import json


logger = logging.getLogger(__name__)


class ConfigurationEnviron(Configuration):
    def __init__(self, variable_regex="CONF"):
        super(ConfigurationEnviron, self).__init__()
        self._get_var_strings(variable_regex=variable_regex)

    def _get_var_strings(self, variable_regex, to_lower=True, replace_underscores=True, keep_match_prefix=True):
        m = re.compile(variable_regex)
        res = list(filter(lambda kv: m.match(kv[0]) is not None, os.environ.items()))
        res = list(map(lambda kv: (''.join(m.split(kv[0])), kv[1]) , res))
        res = list(map(lambda kv: ('.'.join(filter(lambda x: x != "", kv[0].split("_"))), kv[1]) , res))
        res = list(map(lambda kv: (kv[0].lower(), kv[1]) , res))                       
        # res = list(map(lambda kv: "{} = {}".format(kv[0], json.dumps(kv[1])) , res))
        # res = str(reduce(lambda a, b: a + os.linesep + b, ['{'] + res + ['}']))
        # c = Configuration()
        for key,value in res:
            self[key] = value
