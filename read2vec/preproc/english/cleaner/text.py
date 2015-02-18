class TextCleaner(object):
    def lower(self, text):
        return text.lower()

    def clean(self, text):
        text = self.lower(text)
        return text
