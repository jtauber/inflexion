from collections import defaultdict

from .sandhi import SandhiRule


class StemmingRuleSet:

    def __init__(self):
        # mapping of key to list of rules
        self.key_to_rules = defaultdict(list)
        # a reverse mapping of surface to key, stem pairs
        self.surface_to_key_stem = defaultdict(set)

    def add(self, key, rule):
        r = SandhiRule(rule)
        self.surface_to_key_stem[r.surface].add((key, r.stem))

    def possible_stems(self, form):
        for surface, rules in self.surface_to_key_stem.items():
            if form.endswith(surface):
                for key, stem_ending in rules:
                    yield (key, form[:-len(surface)] + stem_ending)
