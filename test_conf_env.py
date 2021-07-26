import unittest
import textwrap
from .conf_env import ConfigurationEnviron
import os

class TestMethods(unittest.TestCase):
    def test_load_env01(self):
        os.environ["CONF_A_B_C_D"] = "value"
        c = ConfigurationEnviron()
        self.assertEqual(c["a.b.c.d"], "value")
    
    def test_load_env02(self):
        os.environ["CONF_A_B_C_D"] = '["value1", "value2"]'
        c = ConfigurationEnviron()
        val = c["a.b.c.d"]
        res = ["value1", "value2"]
        self.assertEqual(val, res)


    def test_load_env03(self):
        os.environ["CONF_A_B_C_D"] = 'https://domain.com'
        c = ConfigurationEnviron()
        val = c["a.b.c.d"]
        res = 'https://domain.com'
        self.assertEqual(val, res)
        
    def test_load_str04(self):
        os.environ["CONF_A_B_C_D"] = '\"oZWFsdGg=\"'
        c = ConfigurationEnviron()
        val = c["a.b.c.d"]
        res = "oZWFsdGg="
        self.assertEqual(val, res)