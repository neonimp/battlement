# coding: utf-8
import unittest
from battlement.conditions.conditions import precondition, post_condition


class Conditioning(unittest.TestCase):
    def test_precondition(self):
        @precondition((lambda v: isinstance(v, str)), "must_str")
        @precondition((lambda v: isinstance(v, int)), "must_int", 1)
        def test_must_be(must_str, must_int):
            return must_str, must_int

        # self.assertRaises(test_must_be(12, "str"), AssertionError("Precondition failed for test_must_be"))
        self.assertEqual(test_must_be("test", must_int=2), ("test", 2))

    def test_post_condition(self):
        @post_condition((lambda old, new: new == old["a"] + old["b"]), ["a", "b"])
        def test_post(a, b):
            return a + b

        self.assertEqual(test_post(5, 5), 10)


if __name__ == '__main__':
    unittest.main()
