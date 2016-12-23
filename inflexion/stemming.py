from collections import defaultdict
import re

from .sandhi import SandhiRule


class StemmingRuleSet:

    def __init__(self):
        # mapping of key to list of rules
        self.key_to_rules = defaultdict(list)
        # a reverse mapping of surface to key, stem pairs
        self.surface_to_key_stem = defaultdict(set)

    def add(self, key, rule, tags=None):
        r = SandhiRule(rule, tags)
        self.key_to_rules[key].append(r)
        self.surface_to_key_stem[r.surface].add((key, r))
        return r

    def inflect(self, stem, key, tag_filter=None):
        base_endings = []
        default = []
        tag_filter = tag_filter or set()

        for rule in self.key_to_rules[key]:
            skip = False
            for tag in rule.tags:
                if tag[0] == "+" and tag[1:] not in tag_filter:
                    skip = True
                    break
                if tag[0] == "-" and tag[1:] in tag_filter:
                    skip = True
                    break
            if skip:
                continue

            base = rule.match_theme(stem)
            if base is not None:
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
            surface = surface.replace("(", r"\(").replace(")", r"\)")
            m = re.match("(.*)" + surface + "$", form)
            if m:
                for key, rule in rules:
                    m2 = re.match(m.group(1) + "(" + rule.theme + ")", form)
                    yield (key, m.group(1) + m2.group(1) + rule.b)
