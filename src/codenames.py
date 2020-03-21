import itertools
from typing import Iterable, List, Tuple, Any

from src.translate import Translate
from src.word2vec import Word2Vec


class CodeNames:

    def __init__(self, trans: Translate, w2c: Word2Vec, dict_lang='en', source_lang='he', ):
        self.dict_lang = dict_lang
        self.source_lang = source_lang
        self.trans = trans
        self.w2c = w2c

    def find_similar_words_by_keyword(self, key_word: str, words: List[str], num: int) -> Iterable[str]:
        eng_trans = self.trans.get_words_translation(self.source_lang, self.dict_lang,
                                                     [key_word] + words, filter_similar=False)
        selected = []
        key_word, eng_trans = eng_trans[0], eng_trans[1:]
        for group in eng_trans:
            words_score = self.w2c.word_similarity(key_word, group)
            words_score = sorted(words_score, key=lambda kvp: kvp[1], reverse=True)
            selected.append(words_score[0])
        selected.sort(key=lambda kvp: kvp[1])
        selected_eng = selected[-num:]

        print(selected)

        # return back to source lang
        selecte_idx = [[idx for idx, word_group in enumerate(eng_trans) if word in word_group][0]
                       for word,_ in selected_eng]
        selected_source = [words[word_idx] for word_idx in selecte_idx]

        return selected_source

    def get_source_word_from_eng(self, words, exclude=[]):
        # todo - select this better
        translations = self.trans.get_words_translation(self.dict_lang, self.source_lang, words, True)
        return [t for tran in translations for t in tran if t not in exclude]

    def find_best_keyword_for_groups(self, pos_words: Iterable[str], neg_words: Iterable[str],
                                     num: int) -> Tuple[List[str], Tuple[Any, Any]]:
        eng_trans = self.trans.get_words_translation(self.source_lang, self.dict_lang, pos_words + neg_words,
                                                     filter_similar=True)
        eng_trans_pos, eng_trans_neg = eng_trans[:len(pos_words)], eng_trans[len(pos_words):]

        pos_product = list(itertools.product(*eng_trans_pos))
        pos_bi_grams = set(i for sublist in [itertools.combinations(g, 2) for g in pos_product] for i in sublist)
        pos_similarity_dict = self.w2c.create_similarity_dict(pos_bi_grams)
        pos_n_grams = num if num == 2 else \
            set(i for sublist in [tuple(itertools.combinations(g, num)) for g in pos_product] for i in sublist)
        similarity = [(ng, pos_similarity_dict.get(ng)) for ng in pos_n_grams]

        all_neg_words = set(i for sublist in eng_trans_neg for i in sublist)
        similarity_with_neg = [(g, s - self.w2c.get_negative_score_for_group(g, all_neg_words)) for (g, s) in
                               similarity]

        similarity_with_neg.sort(key=lambda ng: ng[1])

        most_related = similarity_with_neg[-1]

        related_word_eng = self.w2c.get_similar_for_groups(most_related[0])
        related_word_source = self.get_source_word_from_eng([related_word_eng])
        return related_word_source, most_related
