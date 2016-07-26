from collections import defaultdict

import re


class Inflexion:

    def __init__(self):
        self.lexicons = []
        self.stemming_rule_sets = []

    def add_lexicon(self, lexicon):
        self.lexicons.append(lexicon)

    def add_stemming_rule_set(self, stemming_rule_set):
        self.stemming_rule_sets.append(stemming_rule_set)

    def generate(self, lemma, key, tag_filter=None):

        tag_filter = tag_filter or set()

        stems = set()
        for lexicon in self.lexicons:
            stems.update(lexicon.find_stems(lemma, key, tag_filter))

        results = defaultdict(list)
        for stem in stems:
            for stemming_rule_set in self.stemming_rule_sets:
                for result in stemming_rule_set.inflect(stem, key, tag_filter):
                    form = result["base"] + result["ending"]
                    results[form].append({
                        "stem": stem,
                        "stemming": result,
                    })

        return results

    def parse(self, form, stem_post_processor=lambda x: x):
        results = set()

        for stemming_rule_set in self.stemming_rule_sets:
            for key, stem in stemming_rule_set.possible_stems(form):
                for lexicon in self.lexicons:
                    for lemma, key_regex, tags in \
                            lexicon.stem_to_lemma_key_regex[
                                stem_post_processor(stem)]:
                        if re.match(key_regex, key):
                            results.add((lemma, key))

        return results
