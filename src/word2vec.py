import itertools
import json
import os
import traceback
from typing import Iterable, Tuple

import numpy
from Levenshtein._levenshtein import distance
from gensim.models import KeyedVectors, Word2Vec
from gensim.models.fasttext import load_facebook_model
import numpy as np


class NGramSimilarityDict:
    def __init__(self):
        self.dict = {}

    def add(self, w1, w2, sim):
        self.dict[hash(w1) + hash(w2)] = sim

    def get(self, n_words):
        bi_grams = set(itertools.combinations(n_words, 2))
        return numpy.average(list(self.dict[hash(w1) + hash(w2)] for w1, w2 in bi_grams))


class Word2Vec:
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        self.kv: KeyedVectors = None

    def load_fastext_model(self, path):
        fb_model = load_facebook_model(path)
        self.wv = fb_model.wv

    def load_gensim_from_vsmlib(self, path):
        # json_path = os.path.join(path, "meta_data.json")
        vector_path = os.path.join(path, "words100.npy")
        vocab_path = os.path.join(path, "words100.vocab")

        # with open(vocab_path,encoding='latin') as file:
        # 	meta_data = json.load(file)

        vectors = np.load(vector_path)

        vocab = list(line.rstrip('\n').split()[0] for line in open(vocab_path, 'r', encoding='utf-8'))

        kv = KeyedVectors(100)
        kv.add(vocab, vectors)

        self.kv = kv

    def load_word2vec_format(self, vector_path):
        file_type = vector_path[-3:]
        if file_type == "txt" or file_type == "bz2":
            kv = KeyedVectors.load_word2vec_format(vector_path, binary=False, unicode_errors='replace')
            kv.save('words100en')
        else:
            kv = KeyedVectors.load(vector_path, mmap='r')
        self.kv = kv

    def word_similarity(self, key_group, words_group):
        scores = []
        for word in key_group:
            for w in words_group:
                try:
                    score = (w, self.kv.similarity(word, w))
                except Exception as e:
                    print(e)
                    score = (w, 0)
                scores.append(score)
        return scores

    def create_similarity_dict(self, bi_grams: Iterable[Tuple[str]]) -> NGramSimilarityDict:
        n_gram_dict = NGramSimilarityDict()
        for t in bi_grams:
            t = tuple(t)
            try:
                sim = self.kv.similarity(t[0], t[1])
            except Exception as e:
                print(e)
                sim = 0
            n_gram_dict.add(t[0], t[1], sim)
        return n_gram_dict

    def get_negative_score_for_group(self, group: Iterable[str], negative: Iterable[str]) -> NGramSimilarityDict:
        group_avg_vector = numpy.average(tuple(self.kv.get_vector(w) for w in group), axis=0)
        neg_value = numpy.average(
            [self.cosine_similarity(self.kv.get_vector(w), group_avg_vector) for w in negative])
        return 0 if np.isnan(neg_value) else neg_value

    def get_similar_for_groups(self, positive: Iterable[str], negative: Iterable[str] = [],
                               top_n=1) -> NGramSimilarityDict:
        most_similar = self.kv.most_similar(positive, negative, top_n * 3, restrict_vocab=250000)
        # filter too similar words
        most_similar = [w for w in most_similar if min([distance(w[0], p) for p in positive]) > 3]
        return most_similar[:top_n]

    def cosine_similarity(self, v1, v2):
        return numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
