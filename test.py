#!/usr/bin/env python3

import unittest

from inflexion.sandhi import SandhiRule
from inflexion.stemming import StemmingRuleSet
from inflexion.lexicon import Lexicon
from inflexion import Inflexion


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
        self.assertEqual(repr(rule), "SandhiRule('a|b>c<d|e')")

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
        self.assertEqual(repr(rule), "SandhiRule('|><|X')")

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

    def test_match_theme_3(self):
        rule = SandhiRule("A|>C<D|E")
        self.assertEqual(rule.match_theme("A"), "A")
        self.assertEqual(rule.match_theme("CA"), "CA")
        self.assertIsNone(rule.match_theme("B"))


class StemmingTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StemmingTest, self).__init__(*args, **kwargs)

    def test_possible_stems_1(self):
        rules = StemmingRuleSet()
        rules.add("foo", "A|B>C<D|E")
        self.assertEqual(list(rules.possible_stems("FACE")), [("foo", "FAB")])

    def test_inflect_1(self):
        rules = StemmingRuleSet()
        r = rules.add("foo", "A|B>C<D|E")
        result = rules.inflect("FAB", "foo")
        self.assertEqual(list(result), [{
            "base": "FA",
            "ending": "CE",
            "rule": r,
            "used_default": False,
        }])

    def test_inflect_2(self):
        rules = StemmingRuleSet()
        r = rules.add("foo", "A|B>C<D|E")
        rules.add("foo", "|>C<D|E")
        result = rules.inflect("FAB", "foo")
        self.assertEqual(list(result), [{
            "base": "FA",
            "ending": "CE",
            "rule": r,
            "used_default": False,
        }])

    def test_inflect_3(self):
        rules = StemmingRuleSet()
        r = rules.add("foo", "|>C<D|E")
        result = rules.inflect("FAB", "foo")
        self.assertEqual(list(result), [{
            "base": "FAB",
            "ending": "CE",
            "rule": r,
            "used_default": True,
        }])


class LexiconTest(unittest.TestCase):

    def test_lexicon(self):
        lexicon = Lexicon()
        lexicon.add("FOO", [("bar", "foo")])
        self.assertEqual(lexicon.lemma_to_stems["FOO"], [("bar", "foo")])
        self.assertEqual(
            lexicon.stem_to_lemma_key_regex["foo"],
            {("FOO", "bar")}
        )

    def test_find_stems(self):
        lexicon = Lexicon()
        lexicon.add("FOO", [("bar", "foo")])
        self.assertEqual(lexicon.find_stems("FOO", "barista"), "foo")


class MainTest(unittest.TestCase):

    def setUp(self):
        lexicon = Lexicon()
        lexicon.add("FOO", [("bar", "foo")])
        rules = StemmingRuleSet()
        rules.add("barista", "|o><|llow")
        self.inflexion = Inflexion()
        self.inflexion.add_lexicon(lexicon)
        self.inflexion.add_stemming_rule_set(rules)

    def test_generate(self):
        self.assertEqual(self.inflexion.generate("FOO", "barista"), {"follow"})

    def test_parse(self):
        self.assertEqual(self.inflexion.parse("follow"), {('FOO', 'barista')})


if __name__ == "__main__":
    unittest.main()
