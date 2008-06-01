# tests for captcha.py

import unittest, sys
from captcha import *


class TestCaptcha(unittest.TestCase):

    def test_AdditionCaptcha(self):
        c = AdditionCaptcha(qty=5, min=5, max=5)
        self.assertEqual(c.check(25), True)
        self.assertEqual(c.check(24), False)
        self.assertEqual(c.check(26), False)
        qst = "5 + 5 + 5 + 5 + 5"
        self.assertEqual(c.question(), qst)

        c = AdditionCaptcha(qty=20, min=10, max=1000)
        answer = reduce(lambda a,b : a + b, c.numbers)
        self.assertEqual(c.check(answer), True)

        c = AdditionCaptcha(qty=2, min=10, max=10, str_ops=True)
        self.assertEqual(c.check(20), True)
        self.assertEqual(c.question(), "10 plus 10")


    def test_SubtractionCaptcha(self):
        c = SubtractionCaptcha(qty=2, min=5, max=5)
        self.assertEqual(c.check(0), True)
        self.assertEqual(c.question(), "5 - 5")

        c = SubtractionCaptcha(qty=10, min=10, max=1000)
        answer = reduce(lambda a,b: a - b, c.numbers)
        self.assertEqual(c.check(answer), True)

        c = SubtractionCaptcha(qty=2, min=10, max=10, str_ops=True)
        self.assertEqual(c.check(0), True)
        self.assertEqual(c.question(), "10 minus 10")


    def test_MultiplicationCaptcha(self):
        c = MultiplicationCaptcha(qty=3, min=10, max=10)
        self.assertEqual(c.check(1000), True)
        self.assertEqual(c.question(), "10 * 10 * 10")
        
        c = MultiplicationCaptcha(qty=10, min=10, max=1000)
        answer = reduce(lambda a,b : a * b , c.numbers)
        self.assertEqual(c.check(answer), True)

        c = MultiplicationCaptcha(qty=2, min=10, max=10, str_ops=True)
        self.assertEqual(c.check(100), True)
        self.assertEqual(c.question(), "10 times 10")


    def test_MissingNumberCaptcha(self):
        c = MissingNumberCaptcha(min=5,max=5)
        self.assertEqual(c.check(5), True)
        



def main(argv=None):
    if argv is None: argv = sys.argv
    unittest.main(argv=["tests.py"])


if __name__ == '__main__':
    main()
