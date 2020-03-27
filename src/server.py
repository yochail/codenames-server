import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from src import word2vec as w2v
from src.codenames import CodeNames
from src.translate import Translate
from src.word2vec import Word2Vec

lib = os.getenv('LIB')
if not lib:
    lib = "wiki2vec"
# wv = w2v.gensim_from_vsmlib("../data/" + lib)
w2v = Word2Vec()
w2v.load_word2vec_format('data/wiki2vec/gen/words100en')
trans = Translate('src/my_config.json')
cn = CodeNames(trans, w2v)

app = Flask(__name__)
CORS(app)


# @app.route('/getTextFromPic',methods=['POST'])
# #@cross_origin(origins=['https://mail.google.com'])
# def parse_text():
#     imgdata = base64.b64decode(str(request.data['img']))
#     image = Image.open(io.BytesIO(imgdata))
#     word = one_word_ocr(image)
#     return jsonify(word)

@app.route('/findcodesfromwords', methods=['POST'])
def find_words():
    data = request.get_json()
    text = data['text']
    number = int(data['number'])
    all_words = data['words']
    choosen_words = cn.find_similar_words_by_keyword(key_word=text, words=all_words, num=number)
    return jsonify(choosen_words)


@app.route('/findwordsforcodes', methods=['POST'])
def find_codes():
    data = request.get_json()
    number = int(data['number'])
    positive = data['positive']
    negative = data['negative']
    choosen_words = cn.find_best_keyword_for_groups(pos_words=positive, neg_words=negative, num=number)
    return jsonify(choosen_words)


if __name__ == "__main__":
    # wv = gen_model.wv
    app.run()  # ssl_context='adhoc')
