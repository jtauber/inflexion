import re


class SandhiRule:

    def __init__(self, rule, tags=None):
        """
        rule is string of form A|B>C<D|E
        tags is set of strings annotating the rule for later filtering, etc.
        """
        self.tags = tags or set()
        self.a, bcd, self.e = rule.split("|")
        self.b, cd = bcd.split(">")
        self.c, self.d = cd.split("<")
        self.theme = self.a
        self.stem = self.a + self.b
        self.suffix = self.d + self.e
        self.distinguisher = self.c + self.e
        self.surface = self.a + self.c + self.e

    def __repr__(self):
        if self.tags:
            return "SandhiRule('{0.a}|{0.b}>{0.c}<{0.d}|{0.e}', " \
                "tags={1})".format(self, self.tags)
        else:
            return "SandhiRule('{0.a}|{0.b}>{0.c}<{0.d}|{0.e}')".format(self)

    def match_theme(self, stem):
        """
        If the given stem matches this rule's stem part, return the theme
        (which may be more than this rule's theme part if this rule's stem part
        is only the rightmost part of the given stem) or return None if stems
        don't match.
        """
        if re.match(".*" + self.stem + "$", stem):
            if self.b:
                return stem[:-len(self.b)]
            else:
                return stem
        else:
            return None
