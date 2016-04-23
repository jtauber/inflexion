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
        self.key_to_rules[key].append(r)
        self.surface_to_key_stem[r.surface].add((key, r.stem))
        return r

    def inflect(self, stem, key):
        base_endings = []
        default = []

        for rule in self.key_to_rules[key]:
            base = rule.match_theme(stem)

            if base:
                if rule.stem:
                    base_endings.append((base, rule.distinguisher, rule))
                else:
                    default.append((base, rule.distinguisher, rule))

        # only use default if there are no other options
        if len(base_endings) == 0 and len(default) > 0:
            used_default = True
            base_endings = default
        else:
            used_default = False

        for base, ending, rule in base_endings:
            yield {
                "base": base,
                "ending": ending,
                "rule": rule,
                "used_default": used_default,
            }

    def possible_stems(self, form):
        for surface, rules in self.surface_to_key_stem.items():
            if form.endswith(surface):
                for key, stem_ending in rules:
                    yield (key, form[:-len(surface)] + stem_ending)
