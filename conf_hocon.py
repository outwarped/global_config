import logging
from .conf import Configuration
import json
from pyhocon import HOCONConverter, ConfigFactory, ConfigTree
from .exceptions import ConfigurationException
from typing import Union, Dict

logger = logging.getLogger(__name__)


class ConfigurationHocon(Configuration):
    def __init__(self, o, use_json:bool=True):
        self.__use_json = use_json
        s = None
        if type(o) is not dict:
            try:
                o = self._to_config_object(o)
            except Exception as e:
                raise ConfigurationException(e)
        super(ConfigurationHocon, self).__init__(o)

    def _to_config_object(self, s) -> 'Configuration':
        if isinstance(s, ConfigTree):
            if self.__use_json:
                return Configuration(json.loads(HOCONConverter.convert(s, 'json')))
            return Configuration(s)
        elif isinstance(s, str):
            fallback_config = ConfigFactory.from_dict({})
            res = ConfigFactory.parse_string(s, resolve=False).with_fallback(fallback_config)
            if self.__use_json:
                return Configuration(json.loads(HOCONConverter.convert(res, 'json')))
            return Configuration(res)
        raise ValueError("Cannot parse value", s)
    
    def write(self, stream, output_format='hocon'):
        config = ConfigFactory.from_dict(self.as_dict())
        res = HOCONConverter.convert(config, output_format='hocon', compact=True)
        stream.write(res)
        
    def append(self, c:Union['Configuration', Dict])->'Configuration':
        try:
            return super(ConfigurationHocon, self).append(c)
        except Exception as e:
            fallback_config = ConfigFactory.from_dict(self.as_dict())
            res = ConfigFactory.parse_string(json.dumps(c.as_dict()), resolve=True).with_fallback(fallback_config)
            if self.__use_json:
                _c = Configuration(json.loads(HOCONConverter.convert(res, 'json')))
                return super(ConfigurationHocon, self).append(_c)
            _c = Configuration(res)
            return super(ConfigurationHocon, self).append(_c)