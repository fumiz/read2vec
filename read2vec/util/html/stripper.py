from html.parser import HTMLParser


# HTML Tag stripper via http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class TagStripper:
    def clean(self, text):
        s = MLStripper()
        s.feed(text)
        return s.get_data()
