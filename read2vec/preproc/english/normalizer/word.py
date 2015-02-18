import nltk


def word(token):
    return token[0]


def pos(token):
    return token[1]


def is_unicode(text):
    return True


def force_decode(text):
    if is_unicode(text):
        return text
    return text.decode()


class WordNormalizer:
    def __init__(self):
        # 好きなstemmerを選択すると良い。例えば次のような選択肢がある。
        # self.stemmer = nltk.LancasterStemmer()
        # self.stemmer = nltk.snowball.EnglishStemmer()
        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    @staticmethod
    def is_verb(token):
        return pos(token).startswith("VB")

    @staticmethod
    def is_valid_token(token):
        return pos(token).isalpha()

    @staticmethod
    def is_noun(token):
        return pos(token).startswith("N")

    # 見出し語化
    def lemmatize(self, token):
        if WordNormalizer.is_verb(token):
            return self.lemmatizer.lemmatize(word(token), 'v'), pos(token)
        if WordNormalizer.is_noun(token):
            return self.lemmatizer.lemmatize(word(token), 'n'), pos(token)
        return token

    def clean_by(self, cleaner, tokens):
        ret = []
        for token in tokens:
            cleaned = cleaner(token)
            if cleaned is None:
                continue
            if word(cleaned) == "":
                continue
            ret.append(cleaned)
        return ret

    def clean(self, tokens):
        cleaners = [
            self.lemmatize,
        ]
        for cleaner in cleaners:
            tokens = self.clean_by(cleaner, tokens)
        return [force_decode(x[0]) for x in tokens]
