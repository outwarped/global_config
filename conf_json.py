import logging
from .conf import Configuration
from .exceptions import ConfigurationException
import json

logger = logging.getLogger(__name__)


class ConfigurationJson(Configuration):
    def __init__(self, stream):
        s = None
        try:
            s = json.loads(stream)
        except Exception as e:
            raise ConfigurationException(e)
        super(ConfigurationJson, self).__init__(s)
