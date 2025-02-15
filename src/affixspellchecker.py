from nltk.corpus import words as nltk_words

class AffixSpellChecker:
    def __init__(self) -> None:
        self.word_set = nltk_words.words()

        self.prefixes = {
            'un', 'in', 're', 'dis', 'over', 'under', 'pre', 'post', 'non', 'sub',
            'inter', 'trans', 'super', 'semi', 'anti', 'mid', 'mis', 'out', 'co'
        }
        self.suffixes = {
            'ing', 'ed', 'er', 'est', 'ful', 'ness', 'less', 'ly', 'able', 'ible',
            'al', 'ial', 'ic', 'ical', 'ious', 'ous', 'ive', 'ative', 'ment', 'ion',
            'ation', 'ity', 'ty', 'ize', 'ise', 'dom', 'ship', 'hood', 'ish', 'fold'
        }

    def P(self, word): 
        "Probability of `word`."
        N=sum(self.word_set.values())
        return self.word_set[word] / N

    def correction(self, word): 
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=P)

    def candidates(self, word): 
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words): 
        "The subset of `words` that appear in the dictionary of word_set."
        return set(w for w in words if w in self.word_set)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))