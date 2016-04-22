from collections import defaultdict


class SandhiRule:
    def __init__(self, rule):
        """
        rule is string of form A|B>C<D|E
        """
        self.a, bcd, self.e = rule.split("|")
        self.b, cd = bcd.split(">")
        self.c, self.d = cd.split("<")
        self.theme = self.a
        self.stem = self.a + self.b
        self.suffix = self.d + self.e
        self.distinguisher = self.c + self.e
        self.surface = self.a + self.c + self.e

    def match_theme(self, stem):
        """
        If the given stem ends with this rule's stem part, return the theme
        (which may be more than this rule's theme part if this rule's stem part
        is only the rightmost part of the given stem) or return None if stems
        don't match.
        """
        if stem.endswith(self.stem):
            if self.b:
                return stem[:-len(self.b)]
            else:
                return stem
        else:
            return None


class SurfaceLookup:
    def __init__(self):
        """
        a reverse mapping of surface to key, stem pairs
        """
        self.suffix_rules = defaultdict(set)

    def add(self, key, rule):
        r = SandhiRule(rule)
        self.suffix_rules[r.surface].add((key, r.stem))

    def possible_stems(self, form):
        for surface, rules in self.suffix_rules.items():
            if form.endswith(surface):
                for key, stem_ending in rules:
                    yield (key, form[:-len(surface)] + stem_ending)
