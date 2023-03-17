import unittest
import datetime
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from mycaching.attempt_three import caching_decorator

extra_mock = MagicMock()


@caching_decorator(100, 10)
def do_something(some_arg: str):
    extra_mock()
    return "123"


class TestOperation(unittest.TestCase):
    def test_caching_everythingok(self):
        do_something("ABCD")
        with do_something.lock:
            value = do_something.cache.get('["ABCD"]')
        self.assertEqual("123", value)

    def test_caching_withexception(self):
        do_something.clear()

        global extra_mock

        extra_mock = MagicMock()

        def raiser():
            raise Exception("Something")

        extra_mock.side_effect = raiser

        with pytest.raises(Exception) as ex:
            do_something("ABCD")

        self.assertEqual("Something", str(ex.value))

    @freeze_time("Jan 14th, 2020", auto_tick_seconds=1)
    def test_caching_expires(self):
        expire_something("DEFGH")
        with do_something.lock:
            value = expire_something.cache.get('["DEFGH"]')
        self.assertEqual("123", value)
        datetime.datetime.now()
        datetime.datetime.now()
        with expire_something.lock:
            value = expire_something.cache.get('["DEFGH"]')
        self.assertEqual(None, value)

    def test_extra_element(self):
        expire_something("A1")
        with do_something.lock:
            value = expire_something.cache.get('["A1"]')
        self.assertEqual("123", value)
        expire_something("A2")
        with expire_something.lock:
            value = expire_something.cache.get('["A1"]')
        self.assertEqual(None, value)
        with expire_something.lock:
            value = expire_something.cache.get('["A2"]')
        self.assertEqual("123", value)


@caching_decorator(max_len=1, max_age_seconds=2)
def expire_something(some_arg: str):
    return "123"
