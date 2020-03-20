import unittest
from src.translate import Translate


class test_translate(unittest.TestCase):

    def test_words_combinations(self):

        translate = tr.get_words_translation("he","en",["פרה"])
        self.assertEqual("cow", translate[0])

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