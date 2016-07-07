"""
autocorrect.py
==============
AutoCorrect is a Python module that is a
special dictionary that has build-in
capabilities for autocorrecting based on
a simple learning-algorithm.

Copyright 2016 Eric Cornelissen
Released under the MIT license

Date: 07.07.2016
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
my_dict.learn_file('text.txt')
x = my_dict.find_word('volumes')
print(x)
