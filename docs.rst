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

``SandhiRules`` can be given a set of tags that can be used later to filter out
results if the rule is only to be used in certain contexts:

>>> r3 = SandhiRule("|α!>α<|μέν", {"+enclitic"})
>>> r3.tags
{'+enclitic'}


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

Rules can be included or excluded based on their tags. A ``+tag`` will only be
used if ``tag`` is used as a filter on ``possible_stems`` or ``inflect``. A
``-tag`` will not be used if ``tag`` is used as a filter.

>>> rules.add("PAI.1P", "|α!>α<|μεν", {"-enclitic"})
SandhiRule('|α!>α<|μεν', tags={'-enclitic'})
>>> rules.add("PAI.1P", "|α!>α<|μέν", {"+enclitic"})
SandhiRule('|α!>α<|μέν', tags={'+enclitic'})

>>> for result in rules.inflect("ἱστα!", "PAI.1P"):
...     print(result['base'] + result['ending'])
ἱσταμεν

>>> for result in rules.inflect("φα!", "PAI.1P", {"enclitic"}):
...     print(result['base'] + result['ending'])
φαμέν

In the above two examples, different rules are triggered depending on whether
the ``"enclitic"`` tag filter is passed in.


lexicon
-------

A ``Lexicon`` is currently a mapping between lemmas and stems where stems
are dictionaries mapping key regexes to stems.

For example, the stems dictionary in the example below maps (for the lemma
παύω) any key matching ``P`` (i.e. present forms) to the stem "παυ" and any key
matching ``A[AM]I`` (i.e. active or middle aorist indicatives) to "ἐπαυσ".

>>> from inflexion.lexicon import Lexicon
>>> lexicon = Lexicon()
>>> lexicon.add("παύω", [
...     ("P", "παυ"),
...     ("I", "ἐπαυ"),
...     ("F[AM]", "παυσ"),
...     ("A[AM][NPDSO]", "παυσ"),
...     ("A[AM]I", "ἐπαυσ"),
...     ("XA", "πεπαυκ"),
...     ("YA", "ἐπεπαυκ"),
...     ("X[MP]", "πεπαυ"),
...     ("Y[MP]", "ἐπεπαυ"),
...     ("AP[NPDSO]", "παυθ"),
...     ("API", "ἐπαυθ"),
...     ("FP", "παυθησ"),
... ])

This can then be used look up a stem (perhaps from
``StemmingRuleSet.possible_stems``) to see what lemma and key regex it could
be:

>>> sorted(lexicon.stem_to_lemma_key_regex["παυσ"])
[('παύω', 'A[AM][NPDSO]'), ('παύω', 'F[AM]')]

Inflexion
---------

``Inflexion`` combines a ``StemmingRuleSet`` and ``Lexicon`` to generate and
parse forms.

>>> from inflexion import Inflexion

>>> inflexion = Inflexion()
>>> inflexion.add_lexicon(lexicon)
>>> inflexion.add_stemming_rule_set(rules)

>>> inflexion.generate("παύω", "PAI.3S")
{'παυει'}

(note that, inflexion itself does not have knowledge of Ancient Greek
accentuation)

``Inflexion`` can also parse a form with possible lemma / key pairs:

>>> inflexion.parse("παυει")
{('παύω', 'PAI.3S')}

This will return an empty set if no ending matches or if the stem necessary for
any endings is not in the given lexicons.

>>> inflexion.parse("λυει")
set()
