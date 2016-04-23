Documentation for inflexion
===========================


sandhi
------

>>> from inflexion.sandhi import SandhiRule

>>> r1 = SandhiRule("ἐρ|α>ᾷ<ει|")
>>> r1.theme
'ἐρ'
>>> r1.distinguisher
'ᾷ'
>>> r1.stem
'ἐρα'
>>> r1.suffix
'ει'
>>> r1.surface
'ἐρᾷ'

Given a stem and a rule, we can test if the given stem ends with the rule's
stem part and, if so, return the theme. Note this theme will be longer than the
rule's theme part if the rule's stem part is only the rightmost part of the
given stem.

>>> r2 = SandhiRule("|α>ᾷ<ει|")
>>> r2.match_theme("ἐρα")
'ἐρ'

``match_theme`` returns None if the stem does not match.

>>> r2.match_theme("φιλε")

stemming
--------

Sandhi rules can be associated with a key such as a morphological tag and then
surface forms looked up to return possible key, stem pairs.

First we instantiate a ``StemmingRuleSet`` object:

>>> from inflexion.stemming import StemmingRuleSet
>>> rules = StemmingRuleSet()

Then we add a bunch of keyed rules:

>>> rules.add("PAI.3S", "|>ει<ει|")
SandhiRule('|>ει<ει|')
>>> rules.add("PAI.3S", "|ε>εῖ<ει|")
SandhiRule('|ε>εῖ<ει|')
>>> rules.add("PAI.3S", "|ο>οῖ<ει|")
SandhiRule('|ο>οῖ<ει|')
>>> rules.add("PAI.3S", "|α>ᾷ<ει|")
SandhiRule('|α>ᾷ<ει|')
>>> rules.add("PAS.3S", "|α>ᾷ<ῃ|")
SandhiRule('|α>ᾷ<ῃ|')
>>> rules.add("PMI.2S", "|α>ᾷ<εσαι|")
SandhiRule('|α>ᾷ<εσαι|')
>>> rules.add("PMS.2S", "|α>ᾷ<ησαι|")
SandhiRule('|α>ᾷ<ησαι|')

Now we can get the possible key, stem pairs for a particular form:

>>> for parse, stem in sorted(rules.possible_stems("ἐρᾷ")):
...     print(parse, stem)
PAI.3S ἐρα
PAS.3S ἐρα
PMI.2S ἐρα
PMS.2S ἐρα

We can also inflect a given stem according to a given key:

>>> for result in rules.inflect("ἐρα", "PAI.3S"):
...     print(sorted(result.items()))
[('base', 'ἐρ'), ('ending', 'ᾷ'), ('rule', SandhiRule('|α>ᾷ<ει|')), ('used_default', False)]

>>> for result in rules.inflect("φιλε", "PAI.3S"):
...     print(sorted(result.items()))
[('base', 'φιλ'), ('ending', 'εῖ'), ('rule', SandhiRule('|ε>εῖ<ει|')), ('used_default', False)]

>>> for result in rules.inflect("παυ", "PAI.3S"):
...     print(sorted(result.items()))
[('base', 'παυ'), ('ending', 'ει'), ('rule', SandhiRule('|>ει<ει|')), ('used_default', True)]


lexicon
-------

A ``Lexicon`` is currently a mapping between lemmas and stems where stems
are dictionaries mapping key regexes to stems.

For example, the stems dictionary in the example below maps (for the lemma
παύω) any key matching ``P`` (i.e. present forms) to the stem "παυ" and any key
matching ``A[AM]I`` (i.e. active or middle aorist indicatives) to "ἐπαυσ".

>>> from inflexion.lexicon import Lexicon
>>> lexicon = Lexicon()
>>> lexicon.add("παύω", {
...     "P": "παυ",
...     "I": "ἐπαυ",
...     "F[AM]": "παυσ",
...     "A[AM][NPDSO]": "παυσ",
...     "A[AM]I": "ἐπαυσ",
...     "XA": "πεπαυκ",
...     "YA": "ἐπεπαυκ",
...     "X[MP]": "πεπαυ",
...     "Y[MP]": "ἐπεπαυ",
...     "AP[NPDSO]": "παυθ",
...     "API": "ἐπαυθ",
...     "FP": "παυθησ",
... })

This can then be used look up a stem (perhaps from
``StemmingRuleSet.possible_stems``) to see what lemma and key regex it could
be:

>>> sorted(lexicon.stem_to_lemma_key_regex["παυσ"])
[('παύω', 'A[AM][NPDSO]'), ('παύω', 'F[AM]')]
