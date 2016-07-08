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


def get_word_tuple(node, word):
	"""Get a tuple with information about a word in the dictionary"""
	return (word, node['use_count'], node['follows'], node['leads'])

def surrounding_word_tuple(node, word, position):
	append = True
	for index, item in enumerate(node[position]):
		if item[0] == word:
			node[position][index] = (word, item[1] + 1)
			append = False
			break

	if append:
		node[position].append((word, 1))


class AutoCorrect(object):
	def __init__(self, alphabet=ALPHABET):
		self.__ALPHABET__ = alphabet
		self.__ROOT__ = self.__createchar__('root')

	def __charindex__(self, char):
		"""Get the charachter index in the alphabet"""
		try:
			char = char.lower()
			return self.__ALPHABET__.index(char)
		except:
			return -1

	def __createchar__(self, char):
		return {
			'char': char,
			'children': [None] * len(self.__ALPHABET__),
			'follows': [],
			'is_word': False,
			'leads': [],
			'use_count': 0
		}

	def __traverse__(self, node=None, prefix=''):
		"""Get all the words in the dictionary in a list"""
		if node is None:
			node = self.__ROOT__

		collection = []
		for node in node['children']:
			if node is None:
				continue

			if node['is_word']:
				tup = get_word_tuple(node, prefix + node['char'])
				collection.append(tup)

			collection += self.__traverse__(node, prefix + node['char'])

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
			index = self.__charindex__(character)
			newNode = node['children'][index]

			if newNode is None:
				return []

			node = newNode

		return self.__traverse__(node, prefix)

	def find_similar_words(self, word, follows=None, leads=None):
		"""Find words similar to a given word in the dictionary"""
		candidates = []
		candidates += self.__bubblesearch__(word)
		candidates += self.__missingsearch__(word)
		candidates += self.__replacementsearch__(word)

		collection = []
		for word in candidates:
			rating = 0
			if not follows is None:
				followers = word[2]
				for follower in followers:
					if follower[0] == follows:
						rating += follower[1]
						break

			if not leads is None:
				leaders = word[3]
				for leader in leaders:
					if leader[0] == leads:
						rating += leader[1]
						break

			collection.append((word[0], rating))

		collection.sort(key=lambda tup: tup[1], reverse=True)
		return collection

	def find_word(self, word):
		"""Find a word in the dictionary"""
		current_node = self.__ROOT__
		for char in word:
			index = self.__charindex__(char)
			current_node = current_node['children'][index]

			if current_node is None:
				raise LookupError

		if current_node['is_word']:
			return get_word_tuple(current_node, word)
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

		follow = None
		word = None
		lead = text.pop(0)

		text.append(None)

		for i in range(len(text)):
			follow, word, lead = word, lead, text[i]
			self.learn_word(word, follow, lead)

	def learn_word(self, word, follows=None, leads=None):
		"""Learn a new word to the dictionary"""
		current_node = self.__ROOT__
		word = word.lower()

		for i in range(len(word)):
			char = word[i]
			charachter_index = self.__charindex__(char)

			if charachter_index < 0:
				continue

			if current_node['children'][charachter_index] is None:
				current_node['children'][charachter_index] = self.__createchar__(char)

			current_node = current_node['children'][charachter_index]

		current_node['is_word'] = True
		current_node['use_count'] += 1
		if not follows is None:
			surrounding_word_tuple(current_node, follows, 'follows')
		if not leads is None:
			surrounding_word_tuple(current_node, leads, 'leads')


my_dict = AutoCorrect()

my_dict.learn_text('hey my name is anime')
result = my_dict.find_similar_words('anme', 'my', 'is') # We're looking for 'name' over 'anime'
print(result) # 'name' has a weight of 2 while 'anime' has a weight of 0
