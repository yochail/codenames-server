import io
import json
import os
from typing import List, Any

import requests

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
            for o in response:
                translations = [w['normalizedTarget'] for w in o['translations']]

                if filter_similar:
                    # filter similar words in hebrew
                    for word in translations:
                        translations = [w for w in translations if word not in w or w == word]
                if translations:
                    words_res.append(translations)
        return words_res
