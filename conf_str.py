import logging
from exceptions import ConfigurationException
from conf_yaml import ConfigurationYaml
from conf_json import ConfigurationJson
from conf_hocon import ConfigurationHocon
from conf import Configuration

logger = logging.getLogger(__name__)


class ConfigurationStr(Configuration):
    def __init__(self, stream=""):
        c = None
        error = []
        if type(stream) != dict:
            try:
                if c is None:
                    c = ConfigurationJson(stream)
            except Exception as e:
                error.append(e)
            
            try:
                if c is None:
                    c = ConfigurationHocon(stream)
            except Exception as e:
                error.append(e)
            
            try:
                if c is None:
                    c = ConfigurationYaml(stream)
            except Exception as e:
                error.append(e)
            
            if c is None:
                raise ConfigurationException("Configuration cannot be loaded", *error)
        else:
            c = stream
        super(ConfigurationStr, self).__init__(c)
        
    def write(self, stream, output_format='hocon'):
        d = self.as_dict()
        c = ConfigurationHocon(d)
        c.write(stream, output_format='hocon')