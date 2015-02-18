import read2vec.preproc.english.cleaner
import read2vec.preproc.english.segmenter
import read2vec.preproc.english.normalizer
import read2vec.util.html

import nltk


class Processor:
    def __init__(self):
        self.word_cleaner = read2vec.preproc.english.cleaner.WordCleaner()
        self.text_cleaner = read2vec.preproc.english.cleaner.TextCleaner()
        self.html_stripper = read2vec.util.html.TagStripper()
        self.segmenter = read2vec.preproc.english.segmenter.Segmenter()
        self.normalizer = read2vec.preproc.english.normalizer.WordNormalizer()

    def tokenize(self, words):
        return nltk.pos_tag(words)

    def token_is_empty(self, token):
        return token is None or token[0] == ""

    def clean_and_normalize_token(self, token):
        cleaner = self.word_cleaner
        normalizer = self.normalizer
        processors = [
            cleaner.remove_stop_word,
            cleaner.remove_invalid_pos,
            cleaner.only_alphabets,
            normalizer.lemmatize,
            cleaner.remove_short_word,
        ]
        for processor in processors:
            token = processor(token)
            if self.token_is_empty(token):
                return None
        return token

    def clean_and_normalize(self, tokens):
        ret = []
        for token in tokens:
            cleaned_token = self.clean_and_normalize_token(token)
            if cleaned_token is None:
                continue
            ret.append(cleaned_token[0])
        return ret

    # 入力英語文字列を単語のリストに変換する
    def text2words(self, text):
        cleaned_text = self.text_cleaner.clean(self.html_stripper.clean(text))
        words = self.segmenter.segment(cleaned_text)
        tokens = self.tokenize(words)
        return self.clean_and_normalize(tokens)
