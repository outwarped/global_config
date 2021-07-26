import unittest
import textwrap
from .conf import Configuration

class TestMethods(unittest.TestCase):
    def test_case01(self):        
        dict_config = {
          "a": {
            "b": {
              "c": {
                "d": "value"
              }
            }    
          }
        }
        c = Configuration(dict_config)
        self.assertEqual(c["a.b.c.d"], "value")
