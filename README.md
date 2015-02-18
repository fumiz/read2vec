read2vec
=========

ドキュメント群からword2vecモデルを作成するための実験

Prepare
--------------

自然言語処理を必要とするために言語ごとに特有の準備が必要です

### 英語用のリソースを取得する

英文の形態素解析、分かち書きや見出し語化などにNLTKを使っており、
その辞書データを予めダウンロードしておく必要があります。
次のコマンドで適切なリソースを適切なパスに展開します。
デフォルトでは基本となるパスは`~/nltk_data`です。

```
python setup.py pe
```

Usage
--------------

```
pip install -r requirements.txt
export PYTHONPATH=/path/to/read2vec
python trainer.py
```

Testing
--------------

```
python setup.py test
```

Requirements
--------------

* `Python >= 3.4.2`
* unzipコマンド(`python setup.py pe`に必要)

Tips
--------------

pyenvでPython3.4.2をインストールする時に困りそうなこと

### 1. OpenSSLが無いと怒られる

インストールしましょう

```
brew install openssl
```

.zshrcにでも書いておきましょう

```
export LDFLAGS=-L/usr/local/opt/openssl/lib$
export CPPFLAGS=-I/usr/local/opt/openssl/include$
```

### 2. zlibが無いと怒られる

xcode-selectで入れる

```
xcode-select --install
```
