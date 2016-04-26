from collections import defaultdict
import re


class Lexicon:

    def __init__(self):
        # mapping of lemma to stems (dictionary of key regex to stem_set)
        self.lemma_to_stems = {}
        # a reverse mapping of stem to lemma, key regex pairs
        self.stem_to_lemma_key_regex = defaultdict(set)

    def add(self, lemma, stems):
        """
        stems is a list of (key regex, stem_set) pairs
        """
        self.lemma_to_stems[lemma] = stems
        for key_regex, stem_set in stems:
            for stem in stem_set:
                self.stem_to_lemma_key_regex[stem].add((lemma, key_regex))

    def find_stems(self, lemma, key):
        """
        returns a (possibly empty) stem_set for the given lemma and key
        """
        result = set()
        for key_regex, stem_set in self.lemma_to_stems[lemma]:
            if re.match(key_regex, key):
                result = stem_set  # we don't break or return as we want last

        return result
