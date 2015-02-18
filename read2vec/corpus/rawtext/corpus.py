# 単純なテキストファイルのコーパス
# テキストファイル群をgensim用の[['word1', 'word2',], ['wordA', 'wordB']]形式に変換して提供する
# corpus -> save/load
# loadモードとreadモードを切り替える
# というか、loadモードのコーパスクラスとreadモードのコーパスクラスを使い分ける
# つまりloadメソッドを呼ぶとloadモードのコーパスクラスの方をインスタンス化して返すということ
# readモードでは対象のテキストファイルをon the flyで単語リストに変換しながら提供する
# loadモードでは対象のテキストファイルを一行=一単語として認識して提供する

# 元文書 -> コーパスファイル -> word2vec
import os
import codecs
import read2vec.preproc.english


# gensimのCorpusABCは継承していないが、
# イテレータは実装しているのでgensimの各アルゴリズムのパラメータに使用可能。
#
# ファイル群をon-the-flyで単語リストに変換して使用するならreadメソッドを使う。
# ファイル数が少ない場合にお勧め。
#
# 中間ファイルを作成して使いまわす場合は、buildメソッドで中間ファイルを書き出しながら読みこめばOK
# 書き出したファイルは、後でloadメソッドで読み込める。
class Corpus:
    # ファイルリストを受け取り、中間ファイルを作成せずに直接単語リストを提供するコーパスを返す
    @classmethod
    def read(cls, files):
        return ReaderCorpus(files)

    # RawTextCorpus形式のファイルが保存されたディレクトリを指定してコーパスを読み込む
    @classmethod
    def load(cls, dir_path):
        import glob
        pathes = glob.glob(os.path.join(dir_path, '*.rtc'))
        return LoaderCorpus(pathes)

    @classmethod
    def build_and_load(cls, files, dir_path, logger=None):
        cls.build(files, dir_path, logger)
        corpus = cls.load(dir_path)
        corpus.set_logger(logger)
        return corpus

    # ファイルリストを受け取り、RawTextCorpus形式のファイル群に変換して保存する
    # (loadメソッドで読み込める)
    @classmethod
    def build(cls, files, dir_path, logger=None):
        # ReaderCorpusでドキュメントを順番に中間ファイルにして保存していく
        # 最後に、その中間ファイルを参照するLoaderCorpusのインスタンスを返す
        os.makedirs(dir_path, 0o777, True)
        corpus = ReaderCorpus(files)
        corpus.set_logger(logger)
        id = 0
        for doc in corpus.iter():
            words = doc[0]
            source_path = doc[1]
            save_to_rtc(os.path.join(dir_path, "{0}.rtc".format(id)), source_path, words)
            id += 1

    def __init__(self):
        self.logger = void_logger

    def set_logger(self, logger):
        self.logger = logger


class ReaderCorpus(Corpus):
    def __init__(self, files):
        super().__init__()
        self.files = files
        self.processor = read2vec.preproc.english.Processor()

    def __iter__(self):
        for doc in self.iter():
            yield doc[0]

    def iter(self):
        index = 0
        for path in self.files:
            words = self.processor.text2words(read(path))
            if len(words) == 0:
                self.logger(index, path, "words are empty")
                continue
            self.logger(index, path, "analysed")
            index += 1
            yield words, path


class LoaderCorpus(Corpus):
    def __init__(self, files):
        super().__init__()
        self.files = files

    def __iter__(self):
        index = 0
        for path in self.files:
            rtc = load_from_rtc(path)
            source_path = rtc[0]
            words = rtc[1]
            if len(words) == 0:
                self.logger(index, source_path, "words are empty ({0})".format(path))
                continue
            self.logger(index, source_path, "loaded ({0})".format(path))
            index += 1
            yield words


def save_to_rtc(path, source_path, words):
    with open(path, mode='w', encoding='utf-8') as a_file:
        def writeln(text):
            a_file.write('{0}\n'.format(text))
        writeln("# {0}".format(source_path))
        for word in words:
            writeln(word)


# RTC(RawTextCorpus)形式のファイルを読み込む
def load_from_rtc(path):
    def parse_header(line):
        return line.rstrip()[3:]

    def parse_word(line):
        return line.rstrip()

    header = ""
    words = []
    with open(path, encoding='utf-8') as a_file:
        line_number = 0
        for a_line in a_file:
            line_number += 1
            if line_number == 1:
                # 一行目はヘッダ
                header = parse_header(a_line)
                continue
            word = parse_word(a_line)
            if word == "":
                continue
            words.append(word)
    return header, words


def read(path):
    with codecs.open(path, 'rU', 'utf8') as fp:
        return fp.read()


def void_logger(index, path, msg):
    pass
