#!/usr/bin/env python3

import unittest


class DummyTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DummyTest, self).__init__(*args, **kwargs)

    def test_1(self):
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()
