import unittest
from random import random, randint
from typing import Iterable
from unittest.mock import patch, Mock

from mpmath import rand

from src.codenames import Word2Vec, CodeNames
from src.translate import Translate
from src.word2vec import NGramSimilarityDict


class test_integrations(unittest.TestCase):
    w2v = Word2Vec()
    w2v.load_word2vec_format('../data/wiki2vec/gen/words100en')
    trans = Translate('../src/my_config.json')
    cn = CodeNames(trans, w2v)
    words = ['זאב', 'שרשרת', 'יתוש', 'גילוף', 'חווה'
              ,'שפה', 'אהוב', 'ענן', 'לחם', 'מיטה',
           'שני', 'אוכף', 'דלי', 'כלא', 'דם',
           'כחול', 'משחה', 'נשבר', 'קוקיה', 'שטוח',
           'צייד', 'דובדבן', 'לבנה', 'משה', 'צוות']

    #find_best_keyword_for_groups
    #find_similar_words_by_keyword
    def test_find_similar_words_by_keyword(self):
        res = self.cn.find_similar_words_by_keyword('ערפד',self.words,4)
        self.assertEqual(['res'], res)


if __name__ == '__main__':
    unittest.main()
#
#
#  if (__name__ == "__main__"):
#         # filename = "data/word_linear_cbow_100d"
#         gen_model = gensim_from_vsmlib("data/word_linear_cbow_100d")
#         wv = gen_model.wv
#         # similar_from_list(wv,'vampire', np.array([['WEREWOLF', 'CHAIN', 'MOSQUITO', 'CRAFT', 'RANCH'],
#         #                                        ['LIP', 'VALENTINE', 'CLOUD', 'BEARD', 'BUNK'],
#         #                                        ['SECOND', 'SADDLE', 'BUCKET', 'JAIL', 'BLOOD'],
#         #                                        ['POCKET', 'LACE', 'BREAK', 'CUCKOO', 'FLAT'],
#         #                                        ['BUFFY', 'CHERRY', 'CHRISTMAS', 'MOSES', 'TEAM']]), 3)
#
#         # filename = "./data/cc.he.300.bin.gz"
#
#         # wv = load_word2vec_format( "./data/model_heb.txt")
#
#         # wv = gensim_from_vsmlib("./data/gold") #['דובדבן', 'כיס', 'שרוך']
#
#         # wv = load_word2vec_format("./data/he.wiki.bpe.vs200000.d100.w2v.txt")
#
#         # wv = gensim_from_vsmlib("./data/tweeter") #['דובדבן', 'כיס', 'שרוך']
#         # similar_from_list(wv,'מתוק', np.array([['זאב', 'שרשרת', 'יתוש', 'מלאכה', 'חווה'],
#         #                                        ['שפה', 'אהבה', 'ענן', 'זקן', 'גדה'],
#         #                                        ['שניה', 'אוכף', 'דלי', 'כלא', 'דם'],
#         #                                        ['כיס', 'שרוך', 'הפסקה', 'קוקיה', 'שטוח'],
#         #                                        ['באפי', 'דובדבן', 'כריסטמס', 'משה', 'קבוצה']]), 3)
#
#         # res = find_code_words(wv, ['ברוש', 'שרשרת', 'בנימין', 'באפי', 'דם',
#         #                                         'עטלפים', 'אהבה', 'ענן', 'זקן', 'גדה'],negative=
#         #                                         ['שניה', 'אוכף', 'דלי', 'כלא', 'דם',
#         #                                         'כיס', 'שרוך', 'הפסקה', 'קוקיה', 'שטוח',
#         #                                         'באפי', 'דובדבן', 'כריסטמס', 'משה', 'קבוצה'], top_n=30)
#
#         # res = find_code_words2(wv, positive=['WEREWOLF', 'CHAIN', 'MOSQUITO', 'CRAFT', 'RANCH',
#         #                                      'LIP', 'VALENTINE', 'CLOUD', 'BEARD', 'BUNK',
#         #                                      'BUFFY', 'SADDLE', 'BUCKET', 'JAIL', 'BLOOD'],
#         #                        negative=['POCKET', 'LACE', 'BREAK', 'CUCKOO', 'FLAT',
#         #                                  'BUFFY', 'CHERRY', 'CHRISTMAS', 'MOSES', 'TEAM'], top_n=3, threshhold=0.8)
#         #
#         # print(res)
#     # print(wv.n_similarity(['זקן','זאב', 'בנימין'],['הרצל']))
