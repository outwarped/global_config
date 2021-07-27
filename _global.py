from .conf import Configuration
from . import config
c = Configuration()
from .conf_module import ConfigurationModule
c = c + ConfigurationModule(config)
try:
    from .conf_deployment import ConfigurationDeployment
    c = c + ConfigurationDeployment()
except ImportError:
    pass
from .conf_files import ConfigurationFiles
c = c + ConfigurationFiles(".config")
from .conf_env import ConfigurationEnviron
c = c + ConfigurationEnviron()
try:
    from .conf_args import ConfigurationArgs
    c = c + ConfigurationArgs()
except ImportError:
    pass
from .conf_obj import ConfigurationObject
from .version import __version__
c["__version__"] = __version__
