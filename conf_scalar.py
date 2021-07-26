import logging
from .conf import Configuration
from .exceptions import ConfigurationException
import json
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ConfigurationScalar(Configuration):
    def __init__(self, stream):
        s = None
        try:
            s = json.loads(stream)
        except Exception as e:
            pass
        if isinstance(s, dict):
            raise ConfigurationException("invalid scalar value \"{}\"".format(stream))
        
        if not s is None:
            super(ConfigurationScalar, self).__init__(s)
            return

        if self.uri_validator(stream):
            super(ConfigurationScalar, self).__init__(stream)
            return
        
        
        raise ConfigurationException("invalid scalar value \"{}\"".format(stream))

    @staticmethod
    def uri_validator(x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])
        except:
            return False
        
    # @staticmethod
    # def _is_scalar_type(x):
    #     return ( False
    #         or isinstance(x, type(None)) 
    #         or isinstance(x, int) 
    #         or isinstance(x, float) 
    #         or isinstance(x, bytes) 
    #         or isinstance(x, str) 
    #         or isinstance(x, list) 
    #         or isinstance(x, dict) 
    #         )
            