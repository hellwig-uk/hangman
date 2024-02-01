import unittest

import application

class TestLogic(unittest.TestCase):
    def test_cached_art(self):
        output = application.logic.cached_art(1)
        self.assertIsInstance(output, str)
        self.assertGreaterEqual(len(output), 1)

    def test_create_number_choices_range(self):
        self.assertEqual(
            application.logic.create_number_choices_range(1, 2),
            (('1', 1), ('2', 2)),
        )

    def test_set_word_random(self):
        logic = application.logic.Logic()
        logic.set_word_random((2, 2))
        self.assertTrue(logic._word)
        self.assertIn(logic._word.lower(), ['ad', 'id', 'ox'])

    def test_set_word(self):
        provided = "test"
        logic = application.logic.Logic()
        logic.set_word(provided)
        self.assertEqual(logic._word, provided)
    
    def test_fail_set_empty_word(self):
        logic = application.logic.Logic()
        with self.assertRaises(ValueError):
            logic.set_word("")
    
    def test_set_letter(self):
        logic = application.logic.Logic()
        logic.set_word("test")
        self.assertTrue(logic.set_letter("t"))
        self.assertFalse(logic.set_letter("d"))

        # No empty letters
        with self.assertRaises(ValueError):
            logic.set_letter("")

        # Only 1 letter allowed
        with self.assertRaises(ValueError):
            logic.set_letter("ab")

        # No Duplicate letters
        with self.assertRaises(ValueError):
            logic.set_letter("t")
    
    def test_property_wrong(self):
        logic = application.logic.Logic()
        logic.set_word("test")
        logic.set_letter("a")
        self.assertEqual(logic.wrong, "a")

    def test_property_word(self):
        logic = application.logic.Logic()
        logic.set_word("test")
        self.assertEqual(logic.word, "⎵⎵⎵⎵")
        logic.set_letter("t")
        logic.set_letter("s")
        self.assertEqual(logic.word, "t⎵st")

    def test_property_state(self):
        logic = application.logic.Logic()
        logic.set_word("test")
        self.assertEqual(logic.state, application.logic.STATES.STARTED)
        logic.set_letter("t")
        self.assertEqual(logic.state, application.logic.STATES.ALIVE)
        for letter in ["1", "2", "3", "4", "5", "6"]:
            logic.set_letter(letter)
        self.assertEqual(logic.state, application.logic.STATES.DEAD)

        logic = application.logic.Logic()
        logic.set_word("test")
        for letter in "tes":
            logic.set_letter(letter)
        self.assertEqual(logic.state, application.logic.STATES.WON)
    
    def test_property_art(self):
        logic = application.logic.Logic()
        logic.set_word("test")
        self.assertIsInstance(logic.art, str)
        self.assertGreaterEqual(len(logic.art), 1)        






