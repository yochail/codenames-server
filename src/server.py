import os
import traceback
from threading import Thread

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from src import word2vec as w2v
from src.codenames import CodeNames
from src.translate import Translate
from src.word2vec import Word2Vec

class FlaskApp(Flask):

    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.codeNames = self.init_codenames()

    def init_codenames(self):
        try:
            lib = os.getenv('LIB')
            # if not lib:
            #    lib = "wiki2vec"
            # wv = w2v.gensim_from_vsmlib("../data/" + lib)
            w2v = Word2Vec()
            w2v.load_word2vec_format('data/wiki2vec/gen/words100en')
            trans = Translate('src/my_config.json')
            return CodeNames(trans, w2v)
        except Exception as e:
            traceback.print_exc()
            print(e)

app = FlaskApp(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def status():
    return jsonify(success=True)


# @app.route('/getTextFromPic',methods=['POST'])
# #@cross_origin(origins=['https://mail.google.com'])
# def parse_text():
#     imgdata = base64.b64decode(str(request.data['img']))
#     image = Image.open(io.BytesIO(imgdata))
#     word = one_word_ocr(image)
#     return jsonify(word)


@app.route('/findcodesfromwords', methods=['POST'])
def find_words():
    try:
        data = request.get_json()
        text = data['text']
        number = int(data['number'])
        all_words = data['words']
        choosen_words = app.codeNames.find_similar_words_by_keyword(key_word=text, words=all_words, num=number)
        return jsonify(choosen_words)
    except Exception as e:
        traceback.print_exc()
        return abort(500, 'error while executing.')


@app.route('/findwordsforcodes', methods=['POST'])
def find_codes():
    try:
        data = request.get_json()
        number = int(data['number'])
        positive = data['positive']
        negative = data['negative']
        choosen_words = app.codeNames.find_best_keyword_for_groups(pos_words=positive, neg_words=negative, num=number)
        return jsonify(choosen_words)
    except Exception as e:
        traceback.print_exc()
        return abort(500, 'error while executing.')
