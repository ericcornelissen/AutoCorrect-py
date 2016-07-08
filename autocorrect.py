"""
autocorrect.py
==============
AutoCorrect is a Python module that is a
special dictionary that has build-in
capabilities for autocorrecting based on
a simple learning-algorithm.

Copyright 2016 Eric Cornelissen
Released under the MIT license

Date: 08.07.2016
"""

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class CharNode(object):
	def __init__(self, char, alphabet):
		self.char = char
		self.children = [None] * len(alphabet)
		self.is_word = False
		self.use_count = 0

class AutoCorrect(object):
	def __init__(self, alphabet=ALPHABET):
		self.__ROOT__ = CharNode('root', alphabet)
		self.__ALPHABET__ = alphabet

	def __index__(self, char):
		"""Get the charachter index in the alphabet"""
		try:
			char = char.lower()
			return self.__ALPHABET__.index(char)
		except:
			return -1

	def __traverse__(self, node=None, prefix=''):
		"""Get all the words in the dictionary in a list"""
		if node is None:
			node = self.__ROOT__

		collection = []
		for node in node.children:
			if node is None:
				continue

			if node.is_word:
				collection.append((prefix + node.char, node.use_count))

			collection += self.__traverse__(node, prefix + node.char)

		return collection


	def __bubblesearch__(self, word, position=-2):
		"""Find variations of a word where two characters have been swapped"""
		position += 2
		word_length = len(word)

		if position > word_length:
			return []

		collection = []
		for i in range(position, word_length - 1):
			temp = list(word)
			temp[i], temp[i + 1] = temp[i + 1], temp[i]
			temp = ''.join(temp)

			try:
				word_details = self.find_word(temp)
				collection.append(word_details)
			except:
				pass

			collection += self.__bubblesearch__(temp, position + i)

		return collection

	def __missingsearch__(self, word):
		"""Find variations of a word where a letter is missing"""
		collection = []
		prefix = ''
		suffix = word

		for i in range(len(word) + 1):
			for letter in self.__ALPHABET__:
				word = prefix + letter + suffix

				try:
					word_details = self.find_word(word)
					collection.append(word_details)
				except:
					pass

			# Move the prefix and suffix
			try:
				prefix += suffix[0]
				suffix = suffix[1:]
			except:
				pass

		return collection

	def __replacementsearch__(self, word):
		"""Find variations of a word where some letters are wrong"""
		collection = []

		for i in range(len(word)):
			word_list = list(word)
			for letter in self.__ALPHABET__:
				word_list[i] = letter
				temp = ''.join(word_list)

				try:
					word_details = self.find_word(temp)
					collection.append(word_details)
				except:
					pass

		return collection


	def find_longer_words(self, prefix=''):
		"""Find words with a given prefix in the dictionary"""
		node = self.__ROOT__
		charachters = list(prefix)
		for character in charachters:
			index = self.__index__(character)
			newNode = node.children[index]
			if newNode is None:
				return []

			node = newNode

		return self.__traverse__(node, prefix)

	def find_similar_words(self, word):
		"""Find words similar to a given word in the dictionary"""
		collection = []
		collection += self.__bubblesearch__(word)
		collection += self.__missingsearch__(word)
		collection += self.__replacementsearch__(word)
		return collection

	def find_word(self, word):
		"""Find a word in the dictionary"""
		current_node = self.__ROOT__
		for char in word:
			index = self.__index__(char)
			current_node = current_node.children[index]
			if current_node is None:
				raise LookupError

		if current_node.is_word:
			return (word, current_node.use_count)
		else:
			raise LookupError


	def learn_file(self, file):
		"""Learn a set of words from a file"""
		f = open(file)
		text = f.read()
		self.learn_text(text)

	def learn_text(self, text):
		"""Learn a set of words from a string of text"""
		text = text.split()
		for word in text:
			self.learn_word(word)

	def learn_word(self, word):
		"""Learn a new word to the dictionary"""
		current_node = self.__ROOT__
		word = word.lower()

		for i in range(len(word)):
			charachter_index = self.__index__(word[i])
			if charachter_index < 0:
				continue

			if current_node.children[charachter_index] is None:
				current_node.children[charachter_index] = CharNode(word[i], self.__ALPHABET__)

			current_node = current_node.children[charachter_index]

		current_node.is_word = True
		current_node.use_count += 1

my_dict = AutoCorrect()
my_dict.learn_file('~text.txt')
x = my_dict.find_similar_words('bbout') # Looking for 'about'
print(x)
