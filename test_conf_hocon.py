import unittest
import textwrap
from .conf import Configuration
from .conf_hocon import ConfigurationHocon

class TestMethods(unittest.TestCase):
    def test_load_hocon01(self):
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

        c = ConfigurationHocon(hocon_config)
        self.assertEqual(c["a.b.c.d"], "value")
        
    def test_load_hocon02(self):
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

        c = ConfigurationHocon(hocon_config)
        self.assertEqual(c["e"], "value")
    
    def test_load_hocon03(self):
        hocon_config = textwrap.dedent("""
        a = [1, 2]
        """)
        c = ConfigurationHocon(hocon_config)
        val = c["a"]
        res = [1, 2]
        self.assertEqual(val, res)
