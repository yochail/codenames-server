import io
import json
import os
from typing import List, Any

import requests
import numpy as np

REQ_MAX_CHUNK = 10


class Translate():
    def __init__(self, config_file: str = 'my_config.json'):
        url = "{0}/{1}?{2}"
        with open(config_file) as config_file:
            config_json = json.load(config_file)
            config = config_json['translator']
            self.secret: str = config['secret']
            self.translate_endpoint: str = url.format(config['host'], config['translate'], config['query'])
            self.dictionary_endpoint: str = url.format(config['host'], config['dictionary'], config['query'])

    # TODO
    def translate_word_with_context(self, word: str, context: List[str]) -> str:
        request = [{"Text": str + ' ' + ' '.join(context)}]
        res = requests.post(self.translate_endpoint, json=request, headers={"Ocp-Apim-Subscription-Key": self.secret})
        return res.json()["translations"]["text"]

    def get_words_translation(self, from_lng: str, to_lng: str, words: List[str], filter_similar: bool = False) -> List[
        List[str]]:
        words_res = []
        for i in range(0, len(words), REQ_MAX_CHUNK):
            request = [{"Text": w} for w in words[i:i + REQ_MAX_CHUNK]]
            res = requests.post(self.dictionary_endpoint.format(from_lng, to_lng), json=request,
                                headers={"Ocp-Apim-Subscription-Key": self.secret})
            response = res.json()
            for j, o in enumerate(response):
                avg_score = np.mean([w['confidence'] for w in o['translations']])
                translations = [w['normalizedTarget'] for w in o['translations'] if w['confidence'] >= avg_score]

                if filter_similar:
                    # filter similar words in hebrew
                    for word in translations:
                        translations = [w for w in translations if word not in w or w == word]
                translations = self.filter_words(translations, to_lng)
                if translations:
                    words_res.append(translations)
                else:
                    words_res.append([])
                    print(f"\nmissing translation:'{words[i + j]}'")
        return words_res

    def filter_words(self, words, lang):
        return list(w for w in map(lambda w: w.replace(r"\(.*\)", ""), words) if self.lang_filter(w, lang))

    def lang_filter(self, word, lang):
        if lang == 'he':
            return all([0x05BE <= ord(c) <= 0x05F4 for c in word])
        elif lang == 'en':
            return all([0x0061 <= ord(c) <= 0x007A for c in word])
        else:
            return True
