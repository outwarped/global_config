import logging
import operator
import time
from functools import reduce
from typing import Optional, Union, Dict, Collection, Any


logger = logging.getLogger(__name__)


class Configuration(object):
    def __init__(self, c:Optional[Union['Configuration', Dict]]=None):
        """Create Configuration object
        python dict() or another Configuration can be used as source

        Args:
            c (Optional[Union[, optional): Use this object as Configuration source. Defaults to None (empty configuration).
        """
        self._generation = 0
        super(Configuration, self).__init__()
        if c is None:
            self._config_object = dict()
        else:
            self._config_object = c
            if isinstance(c, Configuration) and c._generation != 0:
                self._on_update()
            elif not isinstance(c, Configuration):
                self._on_update()
            
    def _on_update(self, generation=None):
        self._generation = time.time() if generation is None else generation

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
    
    def __eq__(self, other):
        if self._generation == 0 and other is None:
            return True
        return super(Configuration, self).__eq__(other)

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
    
    @staticmethod
    def _is_native(o) -> bool:
        _native = False
        if not _native and isinstance(o, str):
            _native = True
        if not _native and isinstance(o, bytes):
            _native = True
        if not _native and isinstance(o, float):
            _native = True
        if not _native and isinstance(o, int):
            _native = True
        if not _native and isinstance(o, type(None)):
            _native = True
        if not _native and isinstance(o, list):
            _native = True
        if not _native and isinstance(o, dict):
            _native = True
        
        return _native
    
    def as_dict(self)->Optional[Dict]:
        """Returns current configuration object as python dict

        Returns:
            Optional[Dict]: dict representation
        """
        
        if isinstance(self._config_object, Configuration) and (self._is_native(self._config_object._config_object) or not hasattr(self._config_object._config_object, "__iter__")):
            return self._config_object._config_object
        if not hasattr(self._config_object, "__iter__"):
            return self._config_object
        if isinstance(self._config_object, list):
            return self._config_object
        if isinstance(self._config_object, str):
            return self._config_object
        if isinstance(self._config_object, int):
            return self._config_object
        if isinstance(self._config_object, float):
            return self._config_object
        if isinstance(self._config_object, bytes):
            return self._config_object
        # if self._is_native(self._config_object):
        #     return self._config_object
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
        Args:
            path (Union[str,int]): path to get
            convert (Boolean): (deprecated) Embed target into Configuration object if if target element is an iterable
        Returns:
            [type]: [description]
        """
        try:
            if type(path) == int:
                res = operator.getitem(self._config_object, path)
            else:
                res = reduce(operator.getitem, path.split('.'), self._config_object)
            # if convert and ( type(res) == dict or type(res) == list):
            #     res = self._to_config_object(res)
        except (KeyError, TypeError) as e:
            return None
        
        if isinstance(res, Configuration) and self._is_native(res._config_object):
            return res.as_dict()
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
        if item._generation == self._generation:
            c._on_update(0)
        elif item._generation == 0:
            c._on_update(self._generation)
        elif self._generation == 0:
            c._on_update(item._generation)
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
        self._on_update()
    
    # def __setattr__(self, name, value):
    #     if name in ['_config_object']:
    #         super(Configuration, self).__setattr__(name, value)
    #     else:
    #         self.set_at(name, value)
    
    def __len__(self):
        return len(self.as_dict())

            
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