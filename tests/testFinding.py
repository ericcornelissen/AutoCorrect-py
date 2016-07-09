import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.AutoCorrect = AutoCorrect.Dictionary()

	def tearDown(self):
		self.AutoCorrect = None

	# .find_longer_words
	def test_find_one_longer_word(self):
		"""Test to see if the dictionary can find a longer word"""
		self.AutoCorrect.learn_text('a ab')

		expected = [('ab', 1, [('a', 1)], [])]
		actual = self.AutoCorrect.find_longer_words('a')

		self.assertEqual(expected, actual)

	def test_find_two_longer_words(self):
		"""Test to see if the dictionary can find multiple longer words"""
		self.AutoCorrect.learn_text('abc a ab')

		expected = [('ab', 1, [('a', 1)], []), ('abc', 1, [], [('a', 1)])]
		actual = self.AutoCorrect.find_longer_words('a')

		self.assertEqual(expected, actual)

	# .find_similar_words
	def test_find_one_similar_word(self):
		"""Test to see if the dictionary can find a similar word"""
		self.AutoCorrect.learn_word('foobar')

		expected = [('foobar', 0)]
		actual = self.AutoCorrect.find_similar_words('fobar')

		self.assertEqual(expected, actual)

	def test_find_two_similar_words(self):
		"""Test to see if the dictionary can find two similar words"""
		self.AutoCorrect.learn_text('These are not the droids you are looking for')

		expected = [('for', 0), ('not', 0)]
		actual = self.AutoCorrect.find_similar_words('nor')

		self.assertEqual(expected, actual)

	def test_find_similar_words_using_follows(self):
		"""Test to see if the dictionary can find a similar word, using the follows argument"""
		self.AutoCorrect.learn_text('These are not the droids you are looking for')

		expected = [('for', 1), ('not', 0)]
		actual = self.AutoCorrect.find_similar_words('nor', follows='looking')

		self.assertEqual(expected, actual)

	def test_find_similar_words_using_leads(self):
		"""Test to see if the dictionary can find a similar word, using the leads argument"""
		self.AutoCorrect.learn_text('These are not the droids you are looking for')

		expected = [('not', 1), ('for', 0)]
		actual = self.AutoCorrect.find_similar_words('nor', leads='the')

		self.assertEqual(expected, actual)

	# .find_word
	def test_find_word(self):
		"""Test to see if the dictionary can find a word"""
		self.AutoCorrect.learn_word('foobar')

		expected = ('foobar', 1, [], [])
		actual = self.AutoCorrect.find_word('foobar')

		self.assertEqual(expected, actual)

	def test_dont_find_word(self):
		"""Test to see if the dictionary raises if it cannot find a word"""
		self.assertRaises(LookupError,
			self.AutoCorrect.find_word,
			'foobar'
		)

if __name__ == "__main__":
	unittest.main()
