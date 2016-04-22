#!/usr/bin/env python3

import unittest

from inflexion.sandhi import SandhiRule, SurfaceLookup


class SandhiTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(SandhiTest, self).__init__(*args, **kwargs)

    def test_sandhirule_creation_1(self):
        rule = SandhiRule("a|b>c<d|e")
        self.assertEqual(rule.a, "a")
        self.assertEqual(rule.b, "b")
        self.assertEqual(rule.c, "c")
        self.assertEqual(rule.d, "d")
        self.assertEqual(rule.e, "e")
        self.assertEqual(rule.theme, "a")
        self.assertEqual(rule.distinguisher, "ce")
        self.assertEqual(rule.stem, "ab")
        self.assertEqual(rule.suffix, "de")
        self.assertEqual(rule.surface, "ace")

    def test_sandhirule_creation_2(self):
        rule = SandhiRule("|><|X")
        self.assertEqual(rule.a, "")
        self.assertEqual(rule.b, "")
        self.assertEqual(rule.c, "")
        self.assertEqual(rule.d, "")
        self.assertEqual(rule.e, "X")
        self.assertEqual(rule.theme, "")
        self.assertEqual(rule.distinguisher, "X")
        self.assertEqual(rule.stem, "")
        self.assertEqual(rule.suffix, "X")
        self.assertEqual(rule.surface, "X")

    def test_match_theme_1(self):
        rule = SandhiRule("A|B>C<D|E")
        self.assertEqual(rule.match_theme("AB"), "A")
        self.assertEqual(rule.match_theme("CAB"), "CA")
        self.assertIsNone(rule.match_theme("A"))
        self.assertIsNone(rule.match_theme("B"))

    def test_match_theme_2(self):
        rule = SandhiRule("|B>C<D|E")
        self.assertEqual(rule.match_theme("AB"), "A")
        self.assertEqual(rule.match_theme("CAB"), "CA")
        self.assertIsNone(rule.match_theme("A"))
        self.assertEqual(rule.match_theme("B"), "")

    def test_surfacelookup_1(self):
        lookup = SurfaceLookup()
        lookup.add("foo", "A|B>C<D|E")
        self.assertEqual(list(lookup.possible_stems("FACE")), [("foo", "FAB")])


if __name__ == "__main__":
    unittest.main()
