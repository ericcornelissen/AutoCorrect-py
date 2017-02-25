"""
autocorrect.py
==============
AutoCorrect is a Python module that contains
a special dictionary that has build-in
capabilities for autocorrecting based on a
simple learning algorithm.

Copyright 2016 Eric Cornelissen
Released under the MIT license

Date: 25.02.2017
"""

import copy
import json


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'"]
IMPORT_ALPHABET = None
RATING_EQUAL = 6
RATING_FEEDBACK = 3
RATING_FOLLOWS_LEADS = 1


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
	return (
		word,
		node['use_count'],
		node['follows'],
		node['leads'],
		node['feedback']
	)

def get_string(file=None, path=None, string=None):
	"""Get a string of text given a file or path or string"""
	if file is not None:
		path = file.name

	if path is not None:
		f = open(path, 'r')
		string = f.read()
		f.close()

	if string is None:
		raise ValueError

	return string

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
	global IMPORT_ALPHABET

	children = node['children']
	last_index = 0
	none_ranges = []

	for child in children:
		insert_none(child)

		index = char_index(child['char'], IMPORT_ALPHABET)
		none_ranges.append((last_index, index))
		last_index = index + 1

	none_ranges.append((last_index, len(IMPORT_ALPHABET)))
	for tup in none_ranges:
		for i in range(tup[0], tup[1]):
			children.insert(i, None)

	return node

def remove_duplicates(original_list):
	# Thanks to cchristelis (http://stackoverflow.com/a/24085464)
	unique_list = []
	[unique_list.append(obj) for obj in original_list if obj not in unique_list]
	return unique_list

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
			'char': char.lower(),
			'children': [None] * len(self.__ALPHABET__),
			'feedback': [],
			'follows': [],
			'is_word': False,
			'leads': [],
			'use_count': 0
		}

	def __getnode__(self, node, char):
		index = self.__charindex__(char)
		return node['children'][index]

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


	def __bubblesearch__(self, word, node, position=0):
		"""Find variations of a word where two characters have been swapped"""
		i = 0
		collection = []
		for i in range(position, len(word) - 1):
			# Find out if the current node has the next-next characters as child
			swap_node = self.__getnode__(node, word[i + 1])
			if swap_node is not None:
				# Create a string of the word with the two letters swapped
				temp = list(word)
				temp[i], temp[i + 1] = temp[i + 1], temp[i]
				temp = ''.join(temp)

				# Recursivly call BubbleSearch for more results
				collection += self.__bubblesearch__(temp, swap_node, i + 1)

			node = self.__getnode__(node, word[i])
			if node is None:
				# Early out when the end of the word isn't reached
				return collection

		# Check if an exising word is created by adding the last character
		node = self.__getnode__(node, word[-1])
		if node is not None and node['is_word']:
			word_details = get_word_tuple(node, word)
			collection.append(word_details)

		return remove_duplicates(collection)

	def __insertionsearch__(self, word, node, position=0, depth=0):
		"""Find variations of a word where a letter is missing"""
		if depth >= (.25 * len(word)):
			return []

		collection = []
		for i in range(position, len(word) + 1):
			for insert_node in node['children']:
				if insert_node is not None:
					# Construct a string of the word with inserted letter
					alt_word = word[0:i] + insert_node['char'] + word[i:]

					# Extend the collection with a recursive call
					collection += self.__insertionsearch__(
						alt_word,
						insert_node,
						i + 1,
						depth + 1
					)

					# Try to complete the word in the Dictionary tree
					for j in range(i, len(word)):
						insert_node = self.__getnode__(insert_node, word[j])
						if insert_node is None:
							break

					# Remember the word that was found by the insertion
					if insert_node is not None and insert_node['is_word']:
						word_details = get_word_tuple(insert_node, alt_word)
						collection.append(word_details)

			if i >= len(word): # needed because for-loop extends the word length
				break

			node = self.__getnode__(node, word[i])
			if node is None:
				break

		return remove_duplicates(collection)

	def __replacementsearch__(self, word, node, position=0, depth=0):
		"""Find variations of a word where some letters are wrong"""
		if depth >= (.25 * len(word)):
			return []

		collection = []

		for i in range(position, len(word)):
			for alt_node in node['children']:
				if alt_node is not None:
					# Construct a string of the word with replaced letter
					alt_word = word[0:i] + alt_node['char'] + word[i + 1:]

					# Extend the collection with a recursive call
					collection += self.__replacementsearch__(
						alt_word,
						alt_node,
						i + 1,
						depth + 1
					)

					# Try to complete the word in the Dictionary tree
					for j in range(i + 1, len(word)):
						alt_node = self.__getnode__(alt_node, word[j])
						if alt_node is None:
							break

					# Remember the word that was found by the replacement
					if alt_node is not None and alt_node['is_word']:
						word_details = get_word_tuple(alt_node, alt_word)
						collection.append(word_details)

			node = self.__getnode__(node, word[i])
			if node is None:
				break

		return remove_duplicates(collection)

	def __spacesearch__(self, word):
		"""Find words that appear when the word is split in two"""
		collection = []

		word_list = list(word)
		for i in range(len(word)):
			word_1 = ''.join(word_list[:i])
			word_2 = ''.join(word_list[i:])

			try:
				word_1_details = self.find_word(word_1)
				word_2_details = self.find_word(word_2)

				node = self.__createchar__('a')

				for x in word_1_details[3]:
					if x[0] == word_2:
						node['use_count'] = x[1]

				node['follows'] = word_1_details[2]
				node['leads'] = word_2_details[3]

				res = get_word_tuple(node, word_1 + ' ' + word_2)
				collection.append(res)
			except:
				pass

		return remove_duplicates(collection)


	def correct_text(self, text=None, file=None, path=None):
		"""Automatically correct all the words in a text"""
		text = get_string(file, path, text).split()
		text.append(None)

		follow = None
		word = None
		lead = text.pop(0)

		for i in range(len(text)):
			follow, word, lead = word, lead, text[i]

			prefix = ''
			while self.__charindex__(word[0]) < 0:
				prefix = word[0]
				word = word[1:]

			suffix = ''
			while self.__charindex__(word[-1:]) < 0:
				suffix += word[-1:]
				word = word[:-1]

			text[i] = prefix + self.correct_word(word, follow, lead) + suffix

		return ' '.join(text)

	def correct_word(self, word, follows=None, leads=None):
		"""Automatically correct a word"""
		collection = self.find_similar_words(word, follows, leads)
		try:
			return collection[0][0]
		except:
			return word


	def export(self, file=None, path=None):
		"""Export this AutoCorrect dictionary"""
		if file is not None:
			path = file.name

		root = copy.deepcopy(self.__ROOT__)
		export_data = json.dumps({
			'tree': exclude_none(root),
			'alphabet': self.__ALPHABET__
		})

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
		candidates += self.__bubblesearch__(word, self.__ROOT__)
		candidates += self.__insertionsearch__(word, self.__ROOT__)
		candidates += self.__replacementsearch__(word, self.__ROOT__)
		candidates += self.__spacesearch__(word)

		collection = []
		for candidate in candidates:
			rating = 0

			# Increase the rating if the candiate word is the actual word
			if candidate[0] == word:
				rating += RATING_EQUAL

			# Increase rating if the following words are the same
			if follows is not None:
				followers = candidate[2]
				for follower in followers:
					if follower[0] == follows:
						rating += RATING_FOLLOWS_LEADS
						break

			# Increase rating if the leading words are the same
			if leads is not None:
				leaders = candidate[3]
				for leader in leaders:
					if leader[0] == leads:
						rating += RATING_FOLLOWS_LEADS
						break

			# Increase rating based on manual feedback
			try:
				candidate_node = self.__word__(candidate[0])
				for string in candidate_node['feedback']:
					if string == word:
						rating += RATING_FEEDBACK
						break
			except LookupError:
				pass

			# Create a tuple with the suggestion and rating of that suggestion
			tup = (candidate[0], rating)
			if not tup in collection:
				collection.append(tup)

		collection.sort(key=lambda tup: tup[1], reverse=True)
		return collection

	def find_word(self, word):
		"""Find a word in the dictionary"""
		node = self.__word__(word)
		return get_word_tuple(node, word)


	def get_dictionary(self):
		"""Get all the words in the dictionary in a list"""
		return self.__traverse__()


	def learn_text(self, text=None, file=None, path=None):
		"""Learn all words from a string of text"""
		text = get_string(file, path, text).split()
		text.append(None)

		follow = None
		word = None
		lead = text.pop(0)

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
				node = self.__createchar__(char)
				current_node['children'][charachter_index] = node

			current_node = current_node['children'][charachter_index]

		current_node['is_word'] = True
		current_node['use_count'] += 1

		if follows is not None:
			get_surrounding_word_tuple(current_node, follows, 'follows')
		if leads is not None:
			get_surrounding_word_tuple(current_node, leads, 'leads')


	def suggestion_feedback(self, incorrect, suggestion):
		"""Provide manual feedback on suggestions by the Dictionary"""
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
	string = get_string(file, path, string)
	data = json.loads(string)

	global IMPORT_ALPHABET
	IMPORT_ALPHABET = data['alphabet']

	return Dictionary(alphabet=data['alphabet'], root=insert_none(data['tree']))
