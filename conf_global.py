from .conf import Configuration
from . import config as config
from .conf_env import ConfigurationEnviron
from .conf_files import ConfigurationFiles
from .conf_args import ConfigurationArgs
from .conf_module import ConfigurationModule
from .conf_obj import ConfigurationObject
from .conf_deployment import ConfigurationDeployment


c = Configuration()
c = c + ConfigurationDeployment()
c = c + ConfigurationModule(config)
c = c + ConfigurationFiles(".config")
c = c + ConfigurationEnviron()
c = c + ConfigurationArgs()

