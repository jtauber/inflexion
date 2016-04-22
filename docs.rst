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

These rules can be associated with a key such as a morphological tag and then
surface forms looked up to return possible key, stem pairs.

First we instantiate a SurfaceLookup object:

>>> from inflexion.sandhi import SurfaceLookup
>>> lookup = SurfaceLookup()

Then we add a bunch of keyed rules:

>>> lookup.add("PAI.3S", "|>ει<ει|")
>>> lookup.add("PAI.3S", "|ε>εῖ<ει|")
>>> lookup.add("PAI.3S", "|ο>οῖ<ει|")
>>> lookup.add("PAI.3S", "|α>ᾷ<ει|")
>>> lookup.add("PAI.3S", "|α>ᾷ<ει|")
>>> lookup.add("PAS.3S", "|α>ᾷ<ῃ|")
>>> lookup.add("PMI.2S", "|α>ᾷ<εσαι|")
>>> lookup.add("PMS.2S", "|α>ᾷ<ησαι|")

Now we can get the possible key, stem pairs for a particular form:

>>> for parse, stem in sorted(lookup.possible_stems("ἐρᾷ")):
...     print(parse, stem)
PAI.3S ἐρα
PAS.3S ἐρα
PMI.2S ἐρα
PMS.2S ἐρα
