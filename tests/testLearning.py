import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.Dictionary = AutoCorrect.Dictionary()

	def tearDown(self):
		self.Dictionary = None

	# .learn_word
	def test_learn_one_word(self):
		"""Test to see if it learns one word"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_one_word_twice(self):
		"""Test to see if it learns one word twice"""
		self.Dictionary.learn_word('foobar')
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 2, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	def test_learn_two_words(self):
		"""Test to see if it learns two different word"""
		self.Dictionary.learn_word('foo')
		self.Dictionary.learn_word('bar')

		expected = [('bar', 1, [], [], []), ('foo', 1, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	# .learn_text
	def test_learn_text(self):
		"""Test to see if it learns a small piece of text"""
		self.Dictionary.learn_text('hello world')

		expected = [('hello', 1, [], [('world', 1)], []), ('world', 1, [('hello', 1)], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	# .suggestion_feedback
	def test_suggestion_feedback(self):
		"""Test to see if it learns from suggestions feedback"""
		self.Dictionary.learn_text('These are not the droids you are looking for')
		self.Dictionary.suggestion_feedback('nor', 'not')

		expected = [('not', 3), ('for', 0)]
		actual = self.Dictionary.find_similar_words('nor')

		self.assertEqual(expected, actual)

if __name__ == "__main__":
	unittest.main()
