import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.Dictionary = AutoCorrect.Dictionary()
		self.Root = self.Dictionary.__ROOT__

	def tearDown(self):
		self.Dictionary = None
		self.Root = None

	# .__bubblesearch__
	def test_bubblesearch(self):
		"""Test to see if bubble search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__bubblesearch__('foboar', self.Root)
		self.assertEqual(expected, actual)

	# .__insertionsearch__
	def test_insertionsearch(self):
		"""Test to see if insertion search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__insertionsearch__('foobr', self.Root)
		self.assertEqual(expected, actual)

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__insertionsearch__('foar', self.Root)
		self.assertEqual(expected, actual)

	# .__replacementsearch__
	def test_replacementsearch(self):
		"""Test to see if replacement search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__replacementsearch__('boobar', self.Root)
		self.assertEqual(expected, actual)

	# .__spacesearch__
	def test_spacesearch(self):
		"""Test to see if space search works as expected"""
		self.Dictionary.learn_text('foo bar')

		expected = [('foo bar', 1, [], [], [])]
		actual = self.Dictionary.__spacesearch__('foobar')
		self.assertEqual(expected, actual)



if __name__ == "__main__":
	unittest.main()
