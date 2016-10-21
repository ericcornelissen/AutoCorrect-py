import unittest
import AutoCorrect

class testCorrect(unittest.TestCase):
	def setUp(self):
		self.Dictionary = AutoCorrect.Dictionary()

	def tearDown(self):
		self.Dictionary = None

	def test_correct_word_1(self):
		"""Test to see if the dictionary correctly corrects a word"""
		self.Dictionary.learn_text('nor not')

		expected = 'not'
		actual = self.Dictionary.correct_word('noo', follows='nor')

		self.assertEqual(expected, actual)

	def test_correct_word_2(self):
		expected = 'foo bar'
		self.Dictionary.learn_text(expected)

		actual = self.Dictionary.correct_word('foobar')
		self.assertEqual(expected, actual)

	def test_correct_text(self):
		"""Test to see if the dictionary correctly corrects a string of text"""
		expected = 'This sentence has some mistakes in it.'
		self.Dictionary.learn_text(expected)

		actual = self.Dictionary.correct_text(text='Tis setnence hassome mitakes in i.')
		self.assertEqual(expected, actual)
