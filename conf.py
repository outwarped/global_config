import logging
import operator
from functools import reduce
from functools import partial
from .exceptions import ConfigurationException
from typing import Optional, Union, Dict, Collection, Any


logger = logging.getLogger(__name__)


class Configuration(object):
    def __init__(self, c:Optional[Union['Configuration', Dict]]=None):
        """Create Configuration object
        python dict() or another Configuration can be used as source

        Args:
            c (Optional[Union[, optional): Use this object as Configuration source. Defaults to None (empty configuration).
        """
        super(Configuration, self).__init__()
        if c is None:
            self._config_object = dict()    
        else:
            self._config_object = c

    @staticmethod
    def _to_config_object(o:Union['Configuration', Dict]) -> 'Configuration':
        """internal method to convert arbitrary object into Configuration.
        If the object is already a Configuration object then returns the object

        Returns:
            Configuration: a configuration object
        """
        if isinstance(o, Configuration):
            return o
        return Configuration(o)
    
    def __getitem__(self, item):
        return self.get_at(item)

    def __setitem__(self, item, value):
        self.set_at(item, value)
    
    def __iter__(self):
        for key, value in self._config_object.items():
            yield key, value
    
    def __getattr__(self, item):
        try:
            res = getattr(self._config_object, item)
            return res
        except AttributeError:
            return self.get_at(item)
    
    def as_dict(self)->Optional[Dict]:
        """Returns current configuration object as python dict

        Returns:
            Optional[Dict]: dict representation
        """
        d = {}
        for key, value in self._config_object.items():
            _value = value.as_dict() if isinstance(value, Configuration) else value
            d.update({key:_value})
        return d
    
    def __str__(self):
        return str(dict(self))
    
    def __unicode__(self):
        return str(dict(self))
    
    def __repr__(self):
        return str(dict(self))

    def get_at(self, path:str, convert:bool=True)->Optional[Union['Configuration', Any]]:
        """Returns Configuration branch at given address

        Returns:
            [type]: [description]
        """
        try:
            if type(path) == int:
                res = operator.getitem(self._config_object, path)
            else:
                res = reduce(operator.getitem, path.split('.'), self._config_object)
            if convert and ( type(res) == dict or type(res) == list):
                res = self._to_config_object(res)
        except (KeyError, TypeError) as e:
            return None
        return res
    
    def exists(self, path:Union[str,int])->bool:
        """check if given path exists in Configuration

        Args:
            path (Union[str,int]): path to check

        Returns:
            bool: true if path exists
        """
        try:
            if type(path) == int:
                operator.getitem(self._config_object, path)
            else:
                reduce(operator.getitem, path.split('.'), self._config_object)
        except KeyError as e:
            return False
        return True

    def __add__(self, item):
        def merge(source, destination):
            for key, value in source.items():
                if isinstance(value, dict):
                    # get node or create one
                    node = destination.setdefault(key, {})
                    if isinstance(node, dict):
                        merge(value, node)
                    else:
                        destination[key] = value
                else:
                    destination[key] = value
            return destination
        
        if not isinstance(item, Configuration):
            raise ValueError("Value must be of Configuration type", item)
        
        destination = self.as_dict()
        source = item.as_dict()
        
        _type = type(self)
        res = merge(source, destination)
        c = _type(res)
        return c

    # def set_at(self, path, value)->None:
    #     def _setitem(value, path):
    #         return {path: value}
    #     p = path.split('.')
    #     p.reverse()
    #     res = reduce(_setitem, p, value)
    #     c = Configuration(res)
    #     self += c
    #     return self
    
    def set_at(self, path, value)->None:
        value = self._value_convertor(value)            
        key, _sep, _path = path.partition('.')
        if _sep != '':
            _value = self._config_object.setdefault(key, Configuration())
            if isinstance(_value, Configuration):
                _value.set_at(_path, value)
            else:
                c = Configuration(_value)
                c.set_at(_path, value)
                self._config_object[key] = c
        else:
            self._config_object[key] = value
    
    # def __setattr__(self, name, value):
    #     if name in ['_config_object']:
    #         super(Configuration, self).__setattr__(name, value)
    #     else:
    #         self.set_at(name, value)
            
    def write(self, stream):
        raise NotImplementedError

    def _value_convertor(self, o):
        # TODO: Validate for literal type
        # raise ConfigurationException(ValueError(value))
        return o
    
    def append(self, c:Union['Configuration', Dict])->'Configuration':
        """mutates Configuration object by appending Configuration to current object

        Returns:
            Configuration: self, updated object
        """
        source = self._config_object
        destination = c
        if isinstance(self._config_object, dict):
            source = Configuration(self._config_object)
        if isinstance(c, dict):
            destination = Configuration(c)
        self._config_object = source + destination
        return self