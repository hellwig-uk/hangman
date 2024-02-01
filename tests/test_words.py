import unittest

import application

class TestLogic(unittest.TestCase):
    def test_create_word_select_dictionary(self):
        output = application.words.create_word_select_dictionary(
            path=application.words.DEFAULT_WORD_FILE,
        )
        self.assertIn('test', output[4])

    def test_get_word_list(self):
        output = application.words.get_word_list(
            length=(4 ,4),
            path=application.words.DEFAULT_WORD_FILE,
        )
        self.assertIn('test', output)
    
    def test_get_random_word(self):
        candidates = application.words.get_word_list(
            length=(2 ,2),
            path=application.words.DEFAULT_WORD_FILE,
        )


        random = application.words.get_random_word(
            length_from_to=(2 ,2),
            word_file=application.words.DEFAULT_WORD_FILE,
        )

        self.assertIn(random, candidates)
