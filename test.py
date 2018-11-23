import unittest
from app import verify, makeList, checklist
from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import codecs
from contextlib import contextmanager
app = Flask(__name__)
usernames = ["mom", "dad"]
passwords = ["asdf", "1234"]
user = False


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

    def test3(self):
        self.assertEqual(makeList("testEmpty.csv"), "")

    def test4(self):
        filledList = "['test', 'test', 'test']\n"
        self.assertEqual(makeList("testFilled.csv"), filledList)




    # @app.route("/checklist", methods=['POST', 'GET'])
    # def test3(self):
    #     self.assertEqual(checklist(),render_template("checklist.html"))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()