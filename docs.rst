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
>>> rules.add("PAI.3S", "|ε>εῖ<ει|")
>>> rules.add("PAI.3S", "|ο>οῖ<ει|")
>>> rules.add("PAI.3S", "|α>ᾷ<ει|")
>>> rules.add("PAI.3S", "|α>ᾷ<ει|")
>>> rules.add("PAS.3S", "|α>ᾷ<ῃ|")
>>> rules.add("PMI.2S", "|α>ᾷ<εσαι|")
>>> rules.add("PMS.2S", "|α>ᾷ<ησαι|")

Now we can get the possible key, stem pairs for a particular form:

>>> for parse, stem in sorted(rules.possible_stems("ἐρᾷ")):
...     print(parse, stem)
PAI.3S ἐρα
PAS.3S ἐρα
PMI.2S ἐρα
PMS.2S ἐρα
