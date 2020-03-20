import unittest
from random import random, randint
from unittest.mock import patch, Mock

from mpmath import rand

from src.codenames import find_similar_words_by_trans_to_eng
from src.translate import Translate


class test_translate(unittest.TestCase):

    def create_moq_text2vec(self):
        mock_t2v = Mock()
        mock_t2v.word_similarity = lambda word, words_group: tuple((w, i) for i,w in enumerate(words_group))
        return mock_t2v

    def create_moq_translate(self):
        mock_translate = Mock()
        mock_translate.get_words_translation = lambda from_lng, to_lng, words, filter_similar: tuple(
            (w + 'a', w + 'b', w + 'c') for w in words)
        return mock_translate

    def test_words_combinations(self):
        w2v = self.create_moq_text2vec()
        translate = self.create_moq_translate()
        selected = find_similar_words_by_trans_to_eng(w2v, translate, "keyword", ['1', '2', '3', '4'], 3, 'lang')
        self.assertEqual([('2c', 2), ('3c', 2), ('4c', 2)], selected)

        def test_words_combinations_no_duplication(self):
        w2v = self.create_moq_text2vec()
        translate = self.create_moq_translate()
        w2v.word_similarity = lambda word, words_group: tuple((w, randint(0, 10)) for w in words_group)
        selected = find_similar_words_by_trans_to_eng(w2v, translate, "keyword", ['1', '2', '3', '4','5', '6'],4, 'lang')
        words_source = [w[0][0] for w in selected]
        self.assertEqual(len(words_source),len(set(words_source)))

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
