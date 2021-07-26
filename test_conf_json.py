import unittest
import textwrap
from .conf import Configuration
from .conf_json import ConfigurationJson

class TestMethods(unittest.TestCase):
    def test_load_json01(self):
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

        c = ConfigurationJson(json_config)
        self.assertEqual(c["a.b.c.d"], "value")
        
    def test_load_json02(self):
        json_config = textwrap.dedent("""
        1
        """)
        c = ConfigurationJson(json_config)
        val = c.as_dict()
        res = 1
        self.assertEqual(val, res)

    def test_load_json03(self):
        json_config = textwrap.dedent("""
        [1, 2]
        """)
        c = ConfigurationJson(json_config)
        val = c.as_dict()
        res = [1, 2]
        self.assertEqual(val, res)
