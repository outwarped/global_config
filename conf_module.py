import logging
from exceptions import ConfigurationException
from conf_str import ConfigurationStr
from conf import Configuration
import glob

logger = logging.getLogger(__name__)


class ConfigurationModule(Configuration):
    def __init__(self, module):
        c = Configuration()
        error = None
        
        for path in glob.glob("{}/*.config".format(module.__path__[0])):
            try:
                with open(path) as f:
                    str = f.read()
                    c = c + ConfigurationStr(str)
            except ConfigurationException as e:
                error = e
        super(ConfigurationModule, self).__init__(c)
