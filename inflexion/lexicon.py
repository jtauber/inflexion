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

    def find_stems(self, lemma, key,
                   tag_filter=None, stem_post_processor=lambda x: x):
        """
        returns a (possibly empty) stem_set for the given lemma and key
        """
        tag_filter = tag_filter or set()

        prev_key_regex = None
        result = set()

        for key_regex, stem, tags in self.lemma_to_stems[lemma]:
            skip = False
            for tag in tags:
                if tag[0] == "+" and tag[1:] not in tag_filter:
                    skip = True
                    break
                if tag[0] == "-" and tag[1:] in tag_filter:
                    skip = True
                    break
            if skip:
                continue

            if re.match(key_regex, key):
                if key_regex != prev_key_regex:  # this means multiple stems
                    result = set()               # for same key_regex must be
                    prev_key_regex = key_regex   # contiguously added

                result.add(stem_post_processor(stem))

        return result
