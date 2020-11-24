import logging
from exceptions import ConfigurationException
from conf_str import ConfigurationStr
from conf import Configuration
import glob

logger = logging.getLogger(__name__)


class ConfigurationFiles(Configuration):
    def __init__(self, pathname):
        c = Configuration()
        error = None
        for path in glob.glob(pathname):
            try:
                with open(path) as f:
                    c = c + ConfigurationStr(f)
            except ConfigurationException as e:
                error = e
        super(ConfigurationFiles, self).__init__(c)
