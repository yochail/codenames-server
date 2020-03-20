import unittest
from src.translate import Translate


class test_translate(unittest.TestCase):

    def test_dictionary_he_to_en(self):
        tr = Translate(config_file="../src/my_config.json")
        translate = tr.get_words_translation("he","en",["פרה"])
        self.assertEqual("cow", translate[0])

    def test_dictionary_en_to_he(self):
        tr = Translate(config_file="../src/my_config.json")
        translate = tr.get_words_translation("en", "he", ["dog"], True)
        self.assertEqual("כלב", translate[0])

    def test_dictionary_all_words_meanings(self):
        tr = Translate(config_file="../src/my_config.json")
        translate = tr.get_words_translation("he","en", ["שמן"], True)
        self.assertTupleEqual(('oil','fat'), tuple(translate))

        translate = tr.get_words_translation("he", "en", ["שלום"], True)
        for w in ('shalom', 'hello','peace'):
            self.assertIn(w,translate)


if __name__ == '__main__':
    unittest.main()
