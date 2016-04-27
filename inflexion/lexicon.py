from collections import defaultdict
import re


class Lexicon:

    def __init__(self):
        # mapping of lemma to list of (key_regex, stem, tags)
        self.lemma_to_stems = defaultdict(list)
        # a reverse mapping of stem to set of (lemma, key_regex, tags)
        self.stem_to_lemma_key_regex = defaultdict(set)

    def add(self, lemma, key_regex, stem, tags=None):
        tags = tags or set()
        self.lemma_to_stems[lemma].append((key_regex, stem, tags))
        self.stem_to_lemma_key_regex[stem].add(
            # we use tuple(sorted(...)) to make deterministically hashable
            (lemma, key_regex, tuple(sorted(tags))))

    def find_stems(self, lemma, key):
        """
        returns a (possibly empty) stem_set for the given lemma and key
        """
        result = set()
        for key_regex, stem, tags in self.lemma_to_stems[lemma]:
            if re.match(key_regex, key):
                result = {stem}  # we don't break or return as we want last @@@

        return result
