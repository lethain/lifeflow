__license__ = """Copyright (c) 2007 Will R Larson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""


__author__ = "Will R Larson"
__email__ = "lethain at google's email service"
__description__ = "A library for generating simple text-only captchas."
__api__ = """

The API for a captcha is two methods:

check(answer) --> True or False
question --> either a human or html formatted string
             that represents the question being asked
"""

__todo__ = """
MissingColorCaptcha

Optionally encode questions using HTML character entitites

"""



import random


class BaseMathCaptcha(object):
    def __init__(self, qty=2, min=10, max=30, str_ops=False):
        self._str_ops = str_ops
        self._answer = None
        self._question = None
        self.numbers = []
        for i in xrange(qty):
            num = random.randint(min, max)
            self.numbers.append(num)


    def check(self, answer):
        if self._answer is None:
            self._calculate_answer()
        if int(answer) == self._answer:
            return True
        else:
            return False


    def _calculate_answer(self):
        op = self._operation()
        self._answer = reduce(op, self.numbers)


    def question(self):
        if self._question is None:
            str_numbers = []
            for number in self.numbers:
                str_numbers.append(str(number))
            op_string = self._op_string()
            self._question = op_string.join(str_numbers)
        return self._question


class AdditionCaptcha(BaseMathCaptcha):
    'Captcha for addition problems.'

    def _operation(self):
        return lambda a, b: a + b

    def _op_string(self):
        if self._str_ops is True:
            return " plus "
        else:
            return " + "


class SubtractionCaptcha(BaseMathCaptcha):
    'Captcha for subtraction problems.'

    def _operation(self):
        return lambda a, b: a - b

    def _op_string(self):
        if self._str_ops is True:
            return " minus "
        else:
            return " - "


class MultiplicationCaptcha(BaseMathCaptcha):
    'Captcha for multiplication problems.'

    def _operation(self):
        return lambda a, b: a * b

    def _op_string(self):
        if self._str_ops is True:
            return " times "
        else:
            return " * "



class MissingNumberCaptcha(object):
    def __init__(self, min=1, max=4):
        if min == max:
            self._question = ""
            self.missing = min
        else:
            self.missing = random.randint(min, max)
            numbers = range(min-1, max+2)
            if len(numbers) > 0:
                numbers.remove(self.missing)
                numbers = map(lambda x : str(x), numbers)
                self._question = " ".join(numbers)
            else:
                self._question = ""

    def check(self, answer):
        if int(answer) == self.missing:
            return True
        else:
            return False

    def question(self):
        return self._question

    def __str__(self):
        return self.question()
