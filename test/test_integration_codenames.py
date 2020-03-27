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


    def test_find_similar_words_by_keyword(self):
        words = ['זאב', 'שרשרת', 'יתוש', 'גילוף', 'חווה'
            , 'שפה', 'אהוב', 'ענן', 'לחם', 'מיטה',
                 'שני', 'אוכף', 'דלי', 'כלא', 'דם',
                 'כחול', 'משחה', 'נשבר', 'קוקיה', 'שטוח',
                 'צייד', 'דובדבן', 'לבנה', 'משה', 'צוות']
        res = self.cn.find_similar_words_by_keyword('ערפד',self.words,4)
        self.assertSequenceEqual(['דם', 'יתוש', 'צייד', 'זאב'], res)



    def test_find_best_keyword_for_groups(self):
        res = self.cn.find_best_keyword_for_groups(pos_words=['גמל','חבר','אוזן','חבר','שלום','מכשפה','סל','מטאטא','גרגר','חנות']
                                                   ,neg_words=['מרבד'],num=3)
        self.assertSequenceEqual(['דם', 'יתוש', 'צייד', 'זאב'], res)


if __name__ == '__main__':
    unittest.main()
