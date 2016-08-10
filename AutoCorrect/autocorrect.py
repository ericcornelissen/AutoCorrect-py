"""
autocorrect.py
==============
AutoCorrect is a Python module that contains
a special dictionary that has build-in
capabilities for autocorrecting based on a
simple learning algorithm.

Copyright 2016 Eric Cornelissen
Released under the MIT license

Date: 10.08.2016
"""

import copy
import json


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
import_alphabet = None


def char_index(char, alphabet):
	"""Get the index of a character in an alphabet"""
	try:
		char = char.lower()
		return alphabet.index(char)
	except:
		return -1

def exclude_none(node):
	"""Remove None values from a Dictionary for exporting"""
	l = node['children']
	for i in range(len(l) - 1, -1, -1):
		if l[i] is None:
			del l[i]
		else:
			exclude_none(l[i])

	return node

def get_word_tuple(node, word):
	"""Get a tuple with information about a word in the dictionary"""
	return (word, node['use_count'], node['follows'], node['leads'], node['feedback'])

def get_surrounding_word_tuple(node, word, position):
	"""Get a tuple for a leading or following word"""
	append = True
	for index, item in enumerate(node[position]):
		if item[0] == word:
			node[position][index] = (word, item[1] + 1)
			append = False
			break

	if append:
		node[position].append((word, 1))

def insert_none(node):
	"""Re-add None values to an imported Dictionary"""
	global import_alphabet

	children = node['children']
	last_index = 0
	none_ranges = []

	for child in children:
		insert_none(child)

		index = char_index(child['char'], import_alphabet)
		none_ranges.append((last_index, index))
		last_index = index + 1

	none_ranges.append((last_index, len(import_alphabet)))
	for tup in none_ranges:
		for i in range(tup[0], tup[1]):
			children.insert(i, None)

	return node


class Dictionary(object):
	def __init__(self, alphabet=ALPHABET, root=None):
		self.__ALPHABET__ = alphabet

		if root is None:
			self.__ROOT__ = self.__createchar__('root')
		else:
			self.__ROOT__ = root

	def __charindex__(self, char):
		"""Get the charachter index in the alphabet"""
		return char_index(char, self.__ALPHABET__)

	def __createchar__(self, char):
		"""Create a character dictionary"""
		return {
			'char': char,
			'children': [None] * len(self.__ALPHABET__),
			'feedback': [],
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

	def __word__(self, word):
		"""Find a word in the dictionary"""
		current_node = self.__ROOT__
		for char in word:
			index = self.__charindex__(char)
			current_node = current_node['children'][index]

			if current_node is None:
				raise LookupError

		if current_node['is_word']:
			return current_node
		else:
			raise LookupError


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

			for replacement in self.__ALPHABET__:
				word_list[i] = replacement
				new_word = ''.join(word_list)

				try:
					word_details = self.find_word(new_word)
					collection.append(word_details)
				except:
					pass

		return collection


	def export(self, file=None, path=None):
		"""Export this AutoCorrect dictionary"""
		if file is not None:
			path = file.name

		root = copy.deepcopy(self.__ROOT__)
		export_data = json.dumps({'tree': exclude_none(root), 'alphabet': self.__ALPHABET__})

		if path is not None:
			f = open(path, 'w')
			f.write(export_data)
			f.close()
		else:
			return export_data


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
		for candidate in candidates:
			rating = 0

			# Increase rating if the following words are the same
			if follows is not None:
				followers = candidate[2]
				for follower in followers:
					if follower[0] == follows:
						rating += follower[1]
						break

			# Increase rating if the leading words are the same
			if leads is not None:
				leaders = candidate[3]
				for leader in leaders:
					if leader[0] == leads:
						rating += leader[1]
						break

			# Increase the rating if feedback has been given for a correct suggestion
			candidate_node = self.__word__(candidate[0])
			for string in candidate_node['feedback']:
				if string == word:
					rating += 3
					break

			# Create a tuple with the suggestion and rating of that suggestion
			tup = (candidate[0], rating)
			if not tup in collection:
				collection.append(tup)

		collection.sort(key=lambda tup: tup[1], reverse=True)
		return collection

	def find_word(self, word):
		"""Find a word in the dictionary"""
		current_node = self.__word__(word)
		return get_word_tuple(current_node, word)


	def get_dictionary(self):
		"""Get all the words in the dictionary in a list"""
		return self.__traverse__()


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

		if follows is not None:
			get_surrounding_word_tuple(current_node, follows, 'follows')
		if leads is not None:
			get_surrounding_word_tuple(current_node, leads, 'leads')


	def suggestion_feedback(self, incorrect, suggestion):
		"""Manual feedback on suggestions by find_similar_words"""
		node = self.__word__(suggestion)

		try:
			node['feedback'].index(incorrect)
		except:
			node['feedback'].append(incorrect)


	def unlearn(self, word, feedback=None, follows=None, leads=None):
		"""Unlearn a word or something about a word"""
		word = self.__word__(word)
		if feedback is not None:
			try:
				index = word['feedback'].index(feedback)
				word['feedback'].pop(index)
			except:
				pass

		if follows is not None:
			for i in range(len(word['follows'])):
				tup = word['follows'][i]
				if tup[0] == follows:
					word['follows'].pop(i)
					break

		if leads is not None:
			for i in range(len(word['leads'])):
				tup = word['leads'][i]
				if tup[0] == leads:
					word['leads'].pop(i)
					break

		if feedback is None and follows is None and leads is None:
			word['feedback'] = []
			word['follows'] = []
			word['is_word'] = False
			word['leads'] = []
			word['use_count'] = 0


def Import(file=None, path=None, string=None):
	"""Import an AutoCorrect Dictionary"""
	global import_alphabet

	if file is not None:
		path = file.name

	if path is not None:
		f = open(path, 'r')
		string = f.read()
		f.close()

	if string is not None:
		data = json.loads(string)
		import_alphabet = data['alphabet']

		return Dictionary(
			alphabet=data['alphabet'],
			root=insert_none(data['tree'])
		)
	else:
		raise ValueError()
