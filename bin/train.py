import read2vec.preproc.english

text = """This is a pen."""

p = read2vec.preproc.english.Processor()
words = p.text2words(text)

print(words)
