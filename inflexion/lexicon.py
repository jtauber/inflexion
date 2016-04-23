from collections import defaultdict


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
