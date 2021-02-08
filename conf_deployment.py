import logging
from .exceptions import ConfigurationException
from .conf_str import ConfigurationStr
from .conf import Configuration
from pathlib import Path
from os import makedirs, access, W_OK
from os.path import getmtime, dirname
from uuid import uuid4

logger = logging.getLogger(__name__)


class ConfigurationDeployment(Configuration):
    __deployment_parameter_path = "__config.deployment.uuid"
    __deployment_parameter_mtime = "__config.deployment.mtime"
    __deployment_parameter_generation = "__config.deployment.generation"
    
    def __init__(self):
        
        pp = self._get_persistent_path()

        c = ConfigurationStr()
        try:
            with open("{}".format(pp)) as f:
                str = f.read()
                _c = ConfigurationStr(str)
                c = c + _c
        except ConfigurationException as e:
            raise e
        except FileNotFoundError as e:
            error = e
        
        needs_update = self._set_persistent_data(c)

        if needs_update:
            try:
                makedirs(dirname(pp))
            except FileExistsError as e:
                pass
            try:
                with open("{}".format(pp), 'w+') as f:
                    c.write(f)
            except ConfigurationException as e:
                error = e

        super(ConfigurationDeployment, self).__init__(c)

    @classmethod
    def _get_persistent_path(cls)->Path:
        _home = Path.home()
        if not access(_home, W_OK):
            logger.debug("Home is not writable. Maybe running in a cloud environment...")
            _home = "/tmp"
        
        name = ".config"
        module = cls.__module__
        if module is None or module == str.__class__.__module__:
            name = cls.__name__ + '.config'
        else:
            name = module + '.' + cls.__name__ + '.config'
        
        _config_dir = "{home}/.config/py_global_config/{package}/{name}".format(home=_home, package=__package__, name=name)
        return Path(_config_dir)
    
    def _set_persistent_data(self, c:Configuration)->bool:
        _mtime = getmtime(__file__)
        _deployment = c[self.__deployment_parameter_path]
        _deployment_mtime = c[self.__deployment_parameter_mtime]
        _deployment_generation = c[self.__deployment_parameter_generation]
        
        if not _deployment or not _deployment_mtime or _deployment_mtime != _mtime:
            _deployment = str(uuid4())
            c[self.__deployment_parameter_path] = _deployment
            c[self.__deployment_parameter_mtime] = _mtime
            c[self.__deployment_parameter_generation] = 0 if _deployment_generation is None else _deployment_generation + 1
            return True
        return False
