# -*- coding: utf-8 -*-
from distutils.core import setup, Command
import os
import shutil


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


# 英語処理用の環境をセットアップ
class PrepareEnglish(Command):
    user_options = []

    def __init__(self, dist):
        super().__init__(dist)
        self.data_dir = os.path.expanduser("~/__nltk_data")
        self.temp_dir = "./__temp"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def download(self, url, path):
        import subprocess
        subprocess.call(['curl', '-o', path, url])

    def extract(self, zip_path, path):
        import subprocess
        subprocess.call(['unzip', '-d', path, zip_path])

    def path_to_data_dir(self, path):
        return os.path.join(self.data_dir, path)

    def move_to_data_dir(self, from_path, under_dir):
        import subprocess
        to_dir = self.path_to_data_dir(under_dir)
        os.makedirs(to_dir, 0o777, True)
        subprocess.call(['mv', from_path, "{0}/".format(to_dir)])

    def prepare_data_dir(self):
        os.makedirs(self.data_dir, 0o777, True)

    def prepare_temporary_dir(self):
        self.discard_temporary_dir()
        os.makedirs(self.temp_dir, 0o777, True)

    def discard_temporary_dir(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run(self):
        self.prepare_data_dir()
        self.prepare_temporary_dir()

        defenitions = [
            # [準備1]
            # 事前にNLTKのストップワードをダウンロードして置いておく必要がある
            # http://www.nltk.org/nltk_data/
            # http://www.nltk.org/nltk_data/packages/corpora/stopwords.zip
            # だいたいこんな感じにファイルが配置されていればOK
            # ~/nltk_data/corpora/stopwords/english
            {
                'url': 'http://www.nltk.org/nltk_data/packages/corpora/stopwords.zip',
                'extracted_name': 'stopwords',
                'under_dir': 'corpora',
            },
            # [準備2]
            # 分かち書き用の辞書を用意
            # http://www.nltk.org/nltk_data/packages/tokenizers/punkt.zip
            # ~/nltk_data/tokenizers/punkt
            {
                'url': 'http://www.nltk.org/nltk_data/packages/tokenizers/punkt.zip',
                'extracted_name': 'punkt',
                'under_dir': 'tokenizers',
            },
            # [準備3]
            # 形態素解析用の辞書を用意
            # 最大エントロピー
            # http://www.nltk.org/nltk_data/packages/taggers/maxent_treebank_pos_tagger.zip
            # ~/nltk_data/taggers/maxent_treebank_pos_tagger
            {
                'url': 'http://www.nltk.org/nltk_data/packages/taggers/maxent_treebank_pos_tagger.zip',
                'extracted_name': 'maxent_treebank_pos_tagger',
                'under_dir': 'taggers',
            },
            # [準備4]
            # 見出し語化の辞書を用意(wordnet)
            # http://www.nltk.org/nltk_data/packages/corpora/wordnet.zip
            # ~/nltk_data/corpora/wordnet
            {
                'url': 'http://www.nltk.org/nltk_data/packages/corpora/wordnet.zip',
                'extracted_name': 'wordnet',
                'under_dir': 'corpora',
            },
        ]

        for define in defenitions:
            if os.path.exists(os.path.join(self.path_to_data_dir(define['under_dir']), define['extracted_name'])):
                continue
            temp_zip = os.path.join(self.temp_dir, "temp.zip")
            self.download(define['url'], temp_zip)
            self.extract(temp_zip, self.temp_dir)
            self.move_to_data_dir(os.path.join(self.temp_dir, define['extracted_name']), define['under_dir'])

        self.discard_temporary_dir()

setup(
    cmdclass={
        'test': PyTest,
        'pe': PrepareEnglish,
    },
)
