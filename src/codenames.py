import itertools
from typing import Iterable

from src.translate import Translate
from src.word2vec import Word2Vec


def find_similar_words_by_trans_to_eng(w2c: Word2Vec, tran: Translate, key_word: str, words: Iterable[str], num: int,
                                       lang: str) -> Iterable[str]:
    eng_trans = tran.get_words_translation(lang, 'en', words, filter_similar=True)
    selected = []
    for group in eng_trans:
        words_score = w2c.word_similarity(key_word, group)
        words_score = sorted(words_score, key=lambda kvp: kvp[1],reverse=True)
        selected.append(words_score[0])
    selected.sort(key=lambda kvp: kvp[1])
    return selected[-num:]
