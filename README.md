# global_config

## Description

Automatic configuration data discovery in:

* Environment variables
* Local files
* CLI arguments
* python Modules
* Strings

Configuration namespace is accessible as dictionary-like structure

* Path concatenation (`c[foo.bar.key]`)
* supports formats: HOCON, JSON, YAML, PROPERTIES
* Deep namespace merging
* Global configuration namespace

## Examples

### Global configuration namespace

```python
from global_config import c as c
value1 = c["elements.foo1"]  # concatenated path in indices
value2 = c.elements.foo2  # path as object property
```

### Merging namespaces

```python
from global_config import ConfigurationStr
c1 = ConfigurationStr(...)
c2 = ConfigurationStr(...)
c = c1 + c2
```

### Parse String configuration

```python
from global_config import ConfigurationStr
hocon_config = """
{
  # validate with http://www.hoconlint.com
  a.b: {
    c {
      d = "value"
    }
  }
  e = ${a.b.c.d}
}
"""
c = ConfigurationStr(hocon_config)
c['a.b']  # {'c': {'d': 'value'}}
c['a.b.c.d']  # 'value'
c['e']  # 'value'
```

### Parse CLI arguments

```bash
python foo.py --config=args.value=10
```

```python
from global_config import ConfigurationArgs
c = ConfigurationArgs()
c["args.value"]  # 10
```

### Parse Environment variables

```bash
export CONF_somevalue_somemore="10"
python foo.py
```

```python
from global_config import ConfigurationEnviron
c = ConfigurationEnviron(variable_regex="CONF")
c["somevalue.somemore"]  # 10
```

### Autoloading Configuration from Python modules

```txt
project
├───configuration
│   ├── __init__.py
│   └── main.config
└── foo.py
```

`__init__.py`:

```python
import sys
from global_config import ConfigurationModule
from global_config import c
c.append(ConfigurationModule(sys.modules[__name__]))
```

### importing Configuration from Python modules

```txt
project
├───configuration
│   ├── __init__.py
│   └── main.config
└── foo.py
```

`__init__.py` is empty. It is only required to recognise the python package

`foo.py`:

```python
import configuration
from conf_module import ConfigurationModule
c = ConfigurationModule(configuration)
```
