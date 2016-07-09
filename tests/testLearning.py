import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.AutoCorrect = AutoCorrect.Dictionary()

	def tearDown(self):
		self.AutoCorrect = None

	# .learn_word
	def test_learn_one_word(self):
		"""Test to see if it learns one word"""
		self.AutoCorrect.learn_word('foobar')

		expected = [('foobar', 1, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_one_word_twice(self):
		"""Test to see if it learns one word twice"""
		self.AutoCorrect.learn_word('foobar')
		self.AutoCorrect.learn_word('foobar')

		expected = [('foobar', 2, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_two_words(self):
		"""Test to see if it learns two different word"""
		self.AutoCorrect.learn_word('foo')
		self.AutoCorrect.learn_word('bar')

		expected = [('bar', 1, [], []), ('foo', 1, [], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

	# .learn_text
	def test_learn_text(self):
		"""Test to see if it learns a small piece of text"""
		self.AutoCorrect.learn_text('hello world')

		expected = [('hello', 1, [], [('world', 1)]), ('world', 1, [('hello', 1)], [])]
		actual = self.AutoCorrect.get_dictionary()

		self.assertEqual(expected, actual)

if __name__ == "__main__":
	unittest.main()
