import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.Dictionary = AutoCorrect.Dictionary()

	def tearDown(self):
		self.Dictionary = None

	# .unlearn
	def test_unlearn_word(self):
		"""Test to see if the dictionary corretly unlearns a word"""
		self.Dictionary.learn_word('foobar')
		self.Dictionary.unlearn('foobar')

		expected = []
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	def test_unlearn_nonexistent_word(self):
		"""Test to see if a LookupError is thrown when unlearning a nonexisting word"""
		self.assertRaises(LookupError,
			self.Dictionary.unlearn,
			'foobar'
		)

	def test_unlearn_feedback(self):
		"""Test to see if the dictionary correctly unlearns feedback"""
		self.Dictionary.learn_word('foobar')
		self.Dictionary.suggestion_feedback('fobar', 'foobar')
		self.Dictionary.unlearn('foobar', feedback='fobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	def test_unlearn_nonexistent_feedback(self):
		"""Test to see if the dictionary correctly handles nonexisting feedback"""
		self.Dictionary.learn_word('foobar')
		self.Dictionary.unlearn('foobar', feedback='fobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertEqual(expected, actual)

	def test_unlearn_follows(self):
		"""Test to see if the dictionary correctly unlearns follows"""
		self.Dictionary.learn_text('foo bar')
		self.Dictionary.unlearn('bar', follows='foo')

		expected = [('bar', 1, [], [], []), ('foo', 1, [], [('bar', 1)], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertIn(('bar', 1, [], [], []), actual)
		self.assertIn(('foo', 1, [], [('bar', 1)], []), actual)
		#self.assertEqual(expected, actual)

	def test_unlearn_nonexistent_follows(self):
		"""Test to see if the dictionary correctly handles nonexisting follows"""
		self.Dictionary.learn_text('foo bar')
		self.Dictionary.unlearn('bar', follows='bar')

		expected = [('bar', 1, [('foo', 1)], [], []), ('foo', 1, [], [('bar', 1)], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertIn(('bar', 1, [('foo', 1)], [], []), actual)
		self.assertIn(('foo', 1, [], [('bar', 1)], []), actual)
		#self.assertEqual(expected, actual)

	def test_unlearn_leads(self):
		"""Test to see if the dictionary correctly unlearns leads"""
		self.Dictionary.learn_text('foo bar')
		self.Dictionary.unlearn('foo', leads='bar')

		expected = [('bar', 1, [('foo', 1)], [], []), ('foo', 1, [], [], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertIn(('bar', 1, [('foo', 1)], [], []), actual)
		self.assertIn(('foo', 1, [], [], []), actual)
		#self.assertEqual(expected, actual)

	def test_unlearn_nonexistent_leads(self):
		"""Test to see if the dictionary correctly handles nonexisting leads"""
		self.Dictionary.learn_text('foo bar')
		self.Dictionary.unlearn('foo', leads='foo')

		expected = [('bar', 1, [('foo', 1)], [], []), ('foo', 1, [], [('bar', 1)], [])]
		actual = self.Dictionary.get_dictionary()

		self.assertIn(('bar', 1, [('foo', 1)], [], []), actual)
		self.assertIn(('foo', 1, [], [('bar', 1)], []), actual)
		#self.assertEqual(expected, actual)


if __name__ == "__main__":
	unittest.main()
