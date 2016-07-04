ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class CharNode(object):
	def __init__(self, char):
		self.char = char
		self.is_word = False
		self.use_count = 0
		self.children = [None] * len(ALPHABET)

def char_index(char):
	"""Get the charachter index in the alphabet"""
	try:
		char = char.lower()
		return ALPHABET.index(char)
	except:
		return -1

def learn_word(word):
	"""Learn a new word"""
	current_node = ROOT
	word = word.lower()

	for i in range(len(word)):
		charachter_index = char_index(word[i])

		if charachter_index < 0:
			continue

		if current_node.children[charachter_index] is None:
			current_node.children[charachter_index] = CharNode(word[i])

		current_node = current_node.children[charachter_index]

	current_node.is_word = True
	current_node.use_count += 1

ROOT = CharNode('ROOT')
learn_word('hello')
