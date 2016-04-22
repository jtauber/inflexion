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
