import unittest
from app import verify
import csv
from unittest.mock import patch

from contextlib import contextmanager

@contextmanager
def mockRawInput(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input

class MyTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(verify("mom","asdf"), "user is verified")

    def test2(self):
        self.assertEqual(verify("wrong","wrong"), "Username not found")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()