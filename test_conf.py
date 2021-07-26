import unittest
import textwrap
from .conf import Configuration

class TestMethods(unittest.TestCase):
    
    def test_op01(self):        
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
        val = c["a.b.c"]
        res = {"d": "value"}
        self.assertEqual(val, res)

    def test_op02(self):
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
        val = c["a.b.c.d"]
        res = "value"
        self.assertEqual(val, res)
        
    def test_op03(self):
        dict_config1 = {
          "a": {
            "b": {
              "c": {
                "d": "value1"
              }
            }    
          }
        }
        dict_config2 = {
          "a": {
            "b": {
              "e": {
                "f": "value2"
              }
            }    
          }
        }
        c1 = Configuration(dict_config1)
        c2 = Configuration(dict_config2)
        c = c1 + c2
        val = c["a.b.c.d"]
        res = "value1"
        self.assertEqual(val, res)
        val = c["a.b.e.f"]
        res = "value2"
        self.assertEqual(val, res)
        
    def test_op04(self):
        dict_config1 = {
          "a": {
            "b": {
              "c": {
                "d": "value1"
              }
            }    
          }
        }
        dict_config2 = {
          "a": {
            "b": {
              "c": {
                "d": "value2"
              }
            }    
          }
        }
        c1 = Configuration(dict_config1)
        c2 = Configuration(dict_config2)
        c = c1 + c2
        val = c["a.b.c.d"]
        res = "value2"
        self.assertEqual(val, res)
