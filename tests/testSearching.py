import unittest
import AutoCorrect

class testLearn(unittest.TestCase):
	def setUp(self):
		self.Dictionary = AutoCorrect.Dictionary()

	def tearDown(self):
		self.Dictionary = None

	# .__bubblesearch__
	def test_bubblesearch(self):
		"""Test to see if bubble search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__bubblesearch__('foboar') # Switched 'b' and 'o'

		self.assertEqual(expected, actual)

	# .__missingsearch__
	def test_missingsearch(self):
		"""Test to see if missing search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__missingsearch__('foobr') # Missing an 'a'

		self.assertEqual(expected, actual)

	# .__replacementsearch__
	def test_replacementsearch(self):
		"""Test to see if replacement search works as expected"""
		self.Dictionary.learn_word('foobar')

		expected = [('foobar', 1, [], [], [])]
		actual = self.Dictionary.__replacementsearch__('boobar') # Replaced 'f' with 'b'

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
