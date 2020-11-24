class ConfigurationException(Exception):
    def __init__(self, *args, **kwargs):
        super(ConfigurationException, self).__init__(*args, **kwargs)
