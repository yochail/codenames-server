import unittest

import numpy as np

from src.translate import Translate
from src.word2vec import Word2Vec


class test_translate(unittest.TestCase):

    def test_load_word2vec_file(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        self.assertTupleEqual(tuple(np.zeros(5)), tuple(w2v.kv.get_vector('test00')))

    def test_cosine_similarity(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        self.assertTrue(np.isnan(w2v.cosine_similarity(w2v.kv['test00'], w2v.kv['test00'])))
        self.assertEqual(1, w2v.cosine_similarity(w2v.kv['test01'], w2v.kv['test01']))
        self.assertEqual(0, w2v.cosine_similarity(w2v.kv['test01'], w2v.kv['test02']))
        self.assertTrue(np.isclose(0.70710677, w2v.cosine_similarity(w2v.kv['test14'], w2v.kv['test01'])))
        self.assertAlmostEquals(0.70710677, w2v.cosine_similarity(w2v.kv['test14'], w2v.kv['test01']))
        self.assertAlmostEquals(0.4082483, w2v.cosine_similarity(w2v.kv['test245'], w2v.kv['test24']))

    def test_get_similar_for_groups(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        self.assertEqual('test14', w2v.get_similar_for_groups(['test01', 'test04'])[0][0])
        self.assertEqual('test245', w2v.get_similar_for_groups(['test02', 'test04', 'test05'])[0][0])

    def test_get_negative_score_for_group(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        self.assertAlmostEqual(1.0, w2v.get_negative_score_for_group(['test01'], ['test01']))
        self.assertAlmostEqual(0.0, w2v.get_negative_score_for_group(['test01'], ['test02']))
        self.assertAlmostEqual(0.50000006, w2v.get_negative_score_for_group(['test01', 'test02'], ['test14']))
        self.assertAlmostEqual(0.77459663,
                               w2v.get_negative_score_for_group(['test04', 'test04', 'test05'], ['test245']))

    def test_create_similarity_dict(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        dict = w2v.create_similarity_dict(
            [('test01', 'test01'), ('test01', 'test02'), ('test14', 'test02'), ('test14', 'test01')])
        self.assertAlmostEqual(1.0, dict.get(('test01', 'test01')))
        self.assertAlmostEqual(0.0, dict.get(('test01', 'test02')))
        self.assertAlmostEqual(0.23570226, dict.get(('test01', 'test02', 'test14')))

    def test_word_similarity(self):
        w2v = Word2Vec()
        w2v.load_word2vec_format('testword2vec.txt')
        self.assertSequenceEqual((('test01', 1.0), ('test02', 0.0)), tuple(w2v.word_similarity('test01', ['test01','test02'])))
        self.assertAlmostEqual(0.70710677,
                                 w2v.word_similarity('test01', ['test14']).__next__()[1])


if __name__ == '__main__':
    unittest.main()