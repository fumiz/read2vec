import nltk


class Segmenter(object):
    def __init__(self):
        self.tokenize = nltk.tokenize.wordpunct_tokenize

    def separate(self, text):
        return self.tokenize(text)

    def segment(self, text):
        return self.separate(text)
