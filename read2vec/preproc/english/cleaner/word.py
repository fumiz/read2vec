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


class WordCleaner:
    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        # ストップワードを追加したいならここで
        self.stopwords.update(('wasn', 'didn'))

    @staticmethod
    def is_valid_token(token):
        return pos(token).isalpha()

    # 品詞より記号を除去
    def remove_invalid_pos(self, token):
        if not WordCleaner.is_valid_token(token):
            return None
        return token

    def remove_mask_word(self, token):
        # ここで正規表現で消し去る
        return token

    # ストップワードを除去
    def remove_stop_word(self, token):
        if word(token) in self.stopwords:
            return None
        return token

    # アルファベットで構成された文字列以外を除去
    def only_alphabets(self, token):
        if not word(token).isalpha():
            return None
        return token

    # 一文字だけで構成された文字列を除去
    # I'mとかI'dのmやdだけが残ることがあるので対処
    def remove_short_word(self, token):
        if len(word(token)) == 1:
            return None
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

    # 受け取るのはnltk.pos_tagで取得できるトークンのリスト
    def clean(self, tokens):
        cleaners = [
            self.remove_stop_word,
            self.remove_invalid_pos,
            self.only_alphabets,
            self.remove_short_word
        ]
        for cleaner in cleaners:
            tokens = self.clean_by(cleaner, tokens)
        return [force_decode(x[0]) for x in tokens]
