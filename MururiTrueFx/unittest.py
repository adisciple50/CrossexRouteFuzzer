# TODO - fix unittests

import unittest
from . import truefx

# jsTrader:Ou812:ozrates:1253889202204 - test key

class TestTrueFX(unittest.TestCase):
    def test_login(self):
        self.assertEqual(len(str(truefx.login('jsTrader','Ou812',qualifier='ozrates')).split(':')),4)

    def test_poll(self):
        self.assertEqual(isinstance(truefx.poll('jsTrader:Ou812:ozrates:1253889202204'),str()))

if __name__ == '__main__':
    unittest.main()