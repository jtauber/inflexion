class Inflexion:

    def __init__(self):
        self.lexicons = []
        self.stemming_rule_sets = []

    def add_lexicon(self, lexicon):
        self.lexicons.append(lexicon)

    def add_stemming_rule_set(self, stemming_rule_set):
        self.stemming_rule_sets.append(stemming_rule_set)

    def generate(self, lemma, key):
        stems = set()
        for lexicon in self.lexicons:
            stems.update(lexicon.find_stems(lemma, key))

        results = set()
        for stem in stems:
            for stemming_rule_set in self.stemming_rule_sets:
                for result in stemming_rule_set.inflect(stem, key):
                    results.add(result["base"] + result["ending"])

        return results
