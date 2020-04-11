import itertools
from random import randrange, randint
from typing import Iterable, List, Tuple, Any

import Levenshtein._levenshtein as ld

from src.translate import Translate
from src.word2vec import Word2Vec, NGramSimilarityDict


class CodeNames:

    def __init__(self, trans: Translate, w2v: Word2Vec, dict_lang='en', source_lang='he', ):
        self.dict_lang = dict_lang
        self.source_lang = source_lang
        self.trans = trans
        self.w2v = w2v
        self.names = self.w2v.correct_char_caps(self.names())

    @staticmethod
    def names():
        return ['yaakov', 'yosef', 'shmuel', 'shalom', 'tikva', 'zeev']

    def find_similar_words_by_keyword(self, key_word: str, words: List[str], num: int) -> Iterable[str]:
        eng_trans = self.trans.get_words_translation(self.source_lang, self.dict_lang,
                                                     [key_word] + words, filter_similar=False)
        selected = []
        key_word, eng_trans = eng_trans[0], eng_trans[1:]
        for group in eng_trans:
            words_score = self.w2v.word_similarity(key_word, group)
            words_score = sorted(words_score, key=lambda kvp: kvp[1], reverse=True)
            selected.append(words_score[0])
        selected.sort(key=lambda kvp: kvp[1])
        selected_eng = selected[:num]

        print(selected_eng)

        # return back to source lang
        selecte_idx = [[idx for idx, word_group in enumerate(eng_trans) if word in word_group][0]
                       for word, _ in selected_eng]
        selected_source = [words[word_idx] for word_idx in selecte_idx]

        return selected_source

    def get_source_word_from_eng(self, words, exclude=[]):
        # todo - select this better
        translations = self.trans.get_words_translation(self.dict_lang, self.source_lang, words, True)
        return [t for tran in translations for t in tran if t not in exclude]

    def find_best_keyword_for_groups(self, pos_words: Iterable[str], neg_words: Iterable[str],
                                     num: int) -> Tuple[List[str], Tuple[Any, Any]]:
        print(pos_words)
        eng_trans = self.trans.get_words_translation(self.source_lang, self.dict_lang, pos_words + neg_words,
                                                     filter_similar=True)

        eng_trans = [self.w2v.correct_char_caps(e) for e in eng_trans]
        eng_trans_pos, eng_trans_neg = eng_trans[:len(pos_words)], eng_trans[len(pos_words):]

        print(eng_trans_pos)

        pos_product = list(itertools.product(*[e for e in eng_trans_pos if e]))
        pos_bi_grams = set(i for sublist in [itertools.combinations(g, 2) for g in pos_product] for i in sublist)
        print(pos_bi_grams)
        pos_similarity_dict = self.w2v.create_similarity_dict(pos_bi_grams)


        #choose close worse from positive
        most_related_score = -1
        most_related = None
        if len(eng_trans_pos) > 1:
            while ((most_related_score < 0.5 and num > 1) or not most_related):
                pos_n_grams = pos_bi_grams if num == 2 else \
                    set(i for sublist in [tuple(itertools.combinations(g, num)) for g in pos_product] for i in sublist)
                similarity = [(ng, pos_similarity_dict.get(ng)) for ng in pos_n_grams]

                similarity.sort(key=lambda ng: ng[1],reverse=True)
                #TODO not random
                most_related = similarity[randint(0, min(len(similarity)-1, 2))]
                most_related_score = most_related[1]
                print(most_related)
                num = num - 1
        else:
            most_related = ((eng_trans_pos[0], 1))

        #find sematicly close words
        chosen_word_eng = self.w2v.get_similar_for_groups(most_related[0],[],10)
        print(chosen_word_eng)
        all_neg_words = set(i for sublist in eng_trans_neg for i in sublist if i)
        all_neg_words = all_neg_words.union(set(self.names))
        chosen_word_eng = self.w2v.get_negative_score_for_group(chosen_word_eng,all_neg_words)
        chosen_word_eng.sort(key=lambda ng: ng[1],reverse=True)
        print(chosen_word_eng)

        #get source lang chosen words
        chosen_words_source = self.get_source_word_from_eng([w[0] for w in chosen_word_eng])
        print(chosen_words_source)
        chosen_words_source = self.most_distant_word(chosen_words_source, pos_words)
        print(chosen_words_source)

        #get related word in source lang
        most_related_set = set(most_related[0])
        print(most_related_set)
        most_related_source = [pos_words[i] for i, w in enumerate(eng_trans_pos) if
                               set(w).intersection(most_related_set)]

        print(most_related_source)
        return chosen_words_source, most_related_source

    def most_distant_word(self, words_to_choose, words_origin):
        # avoid similar words- car/cars נהג/מנהיג
        DISTNACE_THRESHOLD = 2
        words = [(word, min([ld.distance(word, w) for w in words_origin])) for word in words_to_choose]
        selected = [w for w in words if w[1] > DISTNACE_THRESHOLD]
        if selected:
            return selected[0][0]
        else:
            return sorted(words, key=lambda w: w[1],reverse=True)[0][0]


