# AutoCorrect
The AutoCorret class is the main class you'll be interacting with when using this Python module. An AutoCorrect instance
is a special dictionary that is able to learn words and autocorrect texts using a simple learning-algorithm.

### `.find_word`
Find a word in the AutoCorrect dictionary. A tuple containing information about that word is
returned if the word is found. Otherwise, if the word wasn't found, a `LookupError` will be thrown.

##### Parameters
| Name | Description                       | Required |
|------|-----------------------------------|----------|
| word | The word you want to find.        | Yes      |

### `.learn_file`
Learn a set of words from a piece of text in a file. If the file is found, all words it can interpret will be learned
by the dictionary. Otherwise, if the file wasn't found, a `FileNotFoundError`  will be thrown.

##### Parameters
| Name | Description                                          | Required |
|------|------------------------------------------------------|----------|
| text | The file containing the text that should be learned. | Yes      |

### `.learn_text`
Learn a set of words from a string of text.

##### Parameters
| Name | Description                                     | Required |
|------|-------------------------------------------------|----------|
| text | The text that should be learned                 | Yes      |

### `.learn_word`
Learn a new word given a string.

##### Parameters
| Name | Description                                       | Required |
|------|---------------------------------------------------|----------|
| word | The word that should be learned by the dictionary | Yes      |
