import unittest
import textwrap
from .conf import Configuration
from .conf_str import ConfigurationStr

class TestMethods(unittest.TestCase):
    def test_load_str01(self):
        json_config = textwrap.dedent("""
        {
          "a": {
            "b": {
              "c": {
                "d": "value" 
                }
              }
            }
          }
        """)

        c = ConfigurationStr(json_config)
        self.assertEqual(c["a.b.c.d"], "value")
    
    def test_load_str02(self):
        hocon_config = textwrap.dedent("""
        {
        # validate with http://www.hoconlint.com
        a.b: {
          c {
            d = "value"
          }
        }
        e = ${a.b.c.d}
        }
        """)

        c = ConfigurationStr(hocon_config)
        self.assertEqual(c["e"], "value")
    
    def test_load_str03(self):
        str_config = textwrap.dedent("""
        [1, 2]
        """)
        c = ConfigurationStr(str_config)
        val = c.as_dict()
        res = [1, 2]
        self.assertEqual(val, res)
        
    def test_load_str04(self):
        str_config = textwrap.dedent("""
        ["1", "2"]
        """)
        c = ConfigurationStr(str_config)
        val = c.as_dict()
        res = ["1", "2"]
        self.assertEqual(val, res)
        
    def test_load_str05(self):
        hocon_config = textwrap.dedent("""
        {
        a : ["1", "2"]
        }
        """)    
        c = ConfigurationStr(hocon_config)
        val = c['a']
        res = ["1", "2"]
        self.assertEqual(val, res)
    
    def test_load_str06(self):
        json_config = textwrap.dedent("""
        {
          "a": {
            "b": {
              "c": {
                "d": "value" 
                }
              }
            }
          }
        """)

        c = ConfigurationStr(json_config)
        val = c['a.b.c']
        res = {"d": "value"}
        self.assertEqual(val, res)
        
    def test_load_str07(self):
        str_config = "\"oZWFsdGg=\""
        c = ConfigurationStr(str_config)
        val = c.as_dict()
        res = "oZWFsdGg="
        self.assertEqual(val, res)
        
    def test_load_str08(self):
        str_config = "\"string\""
        c = ConfigurationStr(str_config)
        val = c.as_dict()
        res = "string"
        self.assertEqual(val, res)