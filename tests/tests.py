import unittest
import AutoCorrect

class testTest(unittest.TestCase):
	def setUp(self):
		self.AutoCorrect = AutoCorrect.Dictionary()

	def tearDown(self):
		self.AutoCorrect = None

	def test_learn_one_word(self):
		"""Test to see if the module correctly learns one word"""
		self.AutoCorrect.learn_word('foobar')

		expected = [('foobar', 1, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_one_word_twice(self):
		"""Test to see if the module correctly learns one word twice"""
		self.AutoCorrect.learn_word('foobar')
		self.AutoCorrect.learn_word('foobar')

		expected = [('foobar', 2, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_two_words(self):
		"""Test to see if the module correctly learns two different word"""
		self.AutoCorrect.learn_word('foo')
		self.AutoCorrect.learn_word('bar')

		expected = [('bar', 1, [], []), ('foo', 1, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

if __name__ == "__main__":
	unittest.main()
