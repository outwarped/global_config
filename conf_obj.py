import logging
from exceptions import ConfigurationException
from conf_str import ConfigurationStr
from conf import Configuration
import glob

logger = logging.getLogger(__name__)


class ConfigurationObject(Configuration):
    def __init__(self, o):
        super(ConfigurationObject, self).__init__(vars(o))
