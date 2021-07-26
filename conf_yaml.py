import logging
from .conf import Configuration
from .exceptions import ConfigurationException
import yaml

logger = logging.getLogger(__name__)


class ConfigurationYaml(Configuration):
    def __init__(self, stream):
        s = None
        try:
            s = yaml.load(stream, Loader=yaml.FullLoader)
        except Exception as e:
            raise ConfigurationException(e)
        super(Configuration, self).__init__(dict(yaml.load(s, Loader=yaml.FullLoader)))
