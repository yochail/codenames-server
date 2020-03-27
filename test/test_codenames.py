import unittest
from random import random, randint
from typing import Iterable
from unittest.mock import patch, Mock

from mpmath import rand

from src.codenames import Word2Vec, CodeNames
from src.translate import Translate
from src.word2vec import NGramSimilarityDict


class test_translate(unittest.TestCase):

    def mock_words_to_Similarity_dict(self, words: Iterable) -> NGramSimilarityDict:
        dict = NGramSimilarityDict()
        for i, t in enumerate(words):
            t = tuple(t)
            dict.add(t[0], t[1], i)
        return dict

    def create_moq_text2vec(self):
        mock_t2v = Mock()
        mock_t2v.word_similarity = lambda word, words_group: tuple((w, i) for i, w in enumerate(words_group))
        mock_t2v.create_similarity_dict = self.mock_words_to_Similarity_dict
        mock_t2v.get_negative_score_for_group.return_value = 1
        mock_t2v.get_similar_for_groups = lambda g1, g2=[], n=1: g1[0]
        return mock_t2v

    def create_moq_translate(self):
        mock_translate = Mock()
        mock_translate.get_words_translation = lambda from_lng, to_lng, words, filter_similar: tuple(
            (w + 'a', w + 'b', w + 'c') for w in words)
        return mock_translate

    def test_words_combinations(self):
        w2v = self.create_moq_text2vec()
        translate = self.create_moq_translate()
        cn = CodeNames(translate, w2v)
        selected = cn.find_similar_words_by_keyword("keyword", ['1', '2', '3', '4'], 3)
        self.assertEqual([('2', 2), ('3', 2), ('4', 2)], selected)

    def test_words_combinations_no_duplication(self):
        w2v = self.create_moq_text2vec()
        translate = self.create_moq_translate()
        cn = CodeNames(translate, w2v)
        w2v.word_similarity = lambda word, words_group: tuple((w, randint(0, 10)) for w in words_group)
        selected = cn.find_similar_words_by_keyword("keyword", ['1', '2', '3', '4', '5', '6'], 4)
        words_source = [w[0][0] for w in selected]
        self.assertEqual(len(words_source), len(set(words_source)))

    def test_find_best_keyword_for_groups(self):
        w2v = self.create_moq_text2vec()
        translate = self.create_moq_translate()
        cn = CodeNames(translate, w2v)
        w2v.word_similarity = lambda word, words_group: tuple((w, randint(0, 10)) for w in words_group)
        selected = cn.find_best_keyword_for_groups(['1', '2', '3', '4'], ['5', '6', '7', '8'], 3)
        self.assertEqual("1ba", selected)


if __name__ == '__main__':
    unittest.main()
