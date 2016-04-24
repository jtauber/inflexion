from collections import defaultdict
import re


class Lexicon:

    def __init__(self):
        # mapping of lemma to stems (dictionary of key regex to stem)
        self.lemma_to_stems = {}
        # a reverse mapping of stem to lemma, key regex pairs
        self.stem_to_lemma_key_regex = defaultdict(set)

    def add(self, lemma, stems):
        """
        stems is a dictionary of key regex to stem
        """
        self.lemma_to_stems[lemma] = stems
        for key_regex, stem in stems.items():
            self.stem_to_lemma_key_regex[stem].add((lemma, key_regex))

    def find_stems(self, lemma, key):
        """
        returns a (possibly empty) set of stems for the given lemma and key
        """
        stems = set()
        for key_regex, stem in self.lemma_to_stems[lemma].items():
            if re.match(key_regex, key):
                stems.add(stem)
        return stems
