import io
import json
import os
from typing import List, Any

import requests

class Translate():
    def __init__(self,config_file:str='my_config.json'):
        url = "{0}/{1}?{2}"
        with open(config_file) as config_file:
            config_json = json.load(config_file)
            config = config_json['translator']
            self.secret:str = config['secret']
            self.translate_endpoint:str = url.format(config['host'],config['translate'],config['query'])
            self.dictionary_endpoint:str = url.format(config['host'],config['dictionary'],config['query'])

    #TODO
    def translate_word_with_context(self,word: str, context: List[str]) -> str:
        request = [{"Text": str + ' ' + ' '.join(context)}]
        res = requests.post(self.translate_endpoint, json=request,headers={"Ocp-Apim-Subscription-Key":self.secret})
        return res.json()["translations"]["text"]

    def get_words_translation(self,from_lng:str,to_lng:str,words: List[str],filter_similar:bool=False) -> List[List[str]]:
        request = [{"Text": w} for w in words]
        res = requests.post(self.dictionary_endpoint.format(from_lng,to_lng), json=request,headers={"Ocp-Apim-Subscription-Key":self.secret})
        response = res.json()
        res: List[List[str]] = []
        for o in response:
            words = [w['normalizedTarget'] for w in o['translations']]

            if filter_similar:
                # filter similar words in hebrew
                for word in words:
                    words = [w for w in words if word not in w or w == word]
            res += words

        return res