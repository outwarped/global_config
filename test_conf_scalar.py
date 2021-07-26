import unittest
import textwrap
from .conf import Configuration
from .conf_scalar import ConfigurationScalar

class TestMethods(unittest.TestCase):
    def test_load_scalar01(self):
        scalar_config = "https://domain.com"
        c = ConfigurationScalar(scalar_config)
        val = c.as_dict()
        res = 'https://domain.com'
        self.assertEqual(val, res)
        
    # def test_load_scalar02(self):
    #     scalar_config = 1
    #     c = ConfigurationScalar(scalar_config)
    #     val = c.as_dict()
    #     res = 1
    #     self.assertEqual(val, res)
