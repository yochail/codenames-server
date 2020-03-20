import os

from flask import Flask, request, jsonify
from flask_cors import CORS

import word2vec as w2v

lib = os.getenv('LIB')
if not lib:
    lib="wiki2vec"
wv = w2v.gensim_from_vsmlib("./data/" + lib)

app = Flask(__name__)
CORS(app)
# @app.route('/getTextFromPic',methods=['POST'])
# #@cross_origin(origins=['https://mail.google.com'])
# def parse_text():
#     imgdata = base64.b64decode(str(request.data['img']))
#     image = Image.open(io.BytesIO(imgdata))
#     word = one_word_ocr(image)
#     return jsonify(word)

@app.route('/findcodesfromwords',methods=['POST'])
def find_words():
    data = request.get_json()
    text = data['text']
    number = int(data['number'])
    all_words = data['words']
    choosen_words = w2v.similar_from_list(wv,text,all_words,number)
    return jsonify(choosen_words)

@app.route('/findwordsforcodes',methods=['POST'])
def find_codes():
    data = request.get_json()
    number = int(data['number'])
    positive = data['positive']
    negative = data['negative']
    choosen_words = w2v.find_code_words(wv,positive=positive,negative=negative,comb_n=number)
    return jsonify(choosen_words)

if __name__ == "__main__":
    #wv = gen_model.wv
    app.run()#ssl_context='adhoc')