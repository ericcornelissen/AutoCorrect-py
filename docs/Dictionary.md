# AutoCorrect.Dictionary
The Dictionary class is the main class you'll be interacting with when using this Python module. A Dictionary instance
is a special dictionary that is able to learn words and autocorrect texts using a simple learning-algorithm.

To get started with this a AutoCorrect dictionary you'll have to create one, this can be done as follows.

```python
import AutoCorrect
my_dictionary = AutoCorrect.Dictionary()
```

#### Parameters
| Name     | Description                                                                   | Required |
|----------|-------------------------------------------------------------------------------|----------|
| alphabet | The alphabet that the Dictionary uses. This is a list of possible characters. | No       |


## Dictionary API
### `.find_longer_words`
Find all words in the AutoCorrect dictionary that start with a given prefix. If no prefix is given, all words in the
dictionary are returned. If there are no words with a given prefix, an empty list is returned.

```python
suggestions = my_dictionary.find_longer_words('foo')
print(suggestions) # Should suggest 'foobar'
```

#### Parameters
| Name   | Description                   | Required |
|--------|-------------------------------|----------|
| prefix | The prefix words should have. | No       |

### `.find_similar_words`
Find all words in the AutoCorrect dictionary that are similar to a given word using several different algorithms.

This method will return an descending (ordered on rating) list of suggestions formatted as a tuple `('word', rating)`,
where the rating is a number that indicates how likely it is the word is the intended word.

```python
suggestions = my_dictionary.find_similar_words('fobar')
print(suggestions) # Should suggest 'foobar'
```

#### Parameters
| Name    | Description                               | Required |
|---------|-------------------------------------------|----------|
| word    | The word for which to find similar words. | Yes      |
| follows | The word the given word follows.          | No       |
| leads   | The word the given word leads.            | No       |

### `.find_word`
Find a word in the AutoCorrect dictionary. A tuple containing information about that word is returned if the word is
found. Otherwise, if the word wasn't found, a `LookupError` will be thrown.

```python
word = my_dictionary.find_word('foobar')
print(word) # information about the 'foobar' (if found)
```

#### Parameters
| Name | Description                       | Required |
|------|-----------------------------------|----------|
| word | The word you want to find.        | Yes      |

### `.get_dictionary`
Get a list of all words in the dictionary. The list contains a tuple for each word with some useful information about
it.

```python
l = my_dictionary.get_dictionary()
print(l) # A list of all the words in my_dictionary
```

### `.learn_file`
Learn a set of words from a piece of text in a file. If the file is found, all words it can interpret will be learned
by the dictionary. Otherwise, if the file wasn't found, a `FileNotFoundError`  will be thrown.

```python
my_dictionary.learn_file('foobar.txt')
```

#### Parameters
| Name | Description                                          | Required |
|------|------------------------------------------------------|----------|
| file | The file containing the text that should be learned. | Yes      |

### `.learn_text`
Learn a set of words from a string of text.

```python
my_dictionary.learn_text('lorem ipsum dolor')
```

#### Parameters
| Name | Description                                     | Required |
|------|-------------------------------------------------|----------|
| text | The text that should be learned.                | Yes      |

### `.learn_word`
Learn a new word given a string.

```python
my_dictionary.learn_word('foobar')
```

#### Parameters
| Name    | Description                                        | Required |
|---------|----------------------------------------------------|----------|
| word    | The word that should be learned by the dictionary. | Yes      |
| follows | A word that tends to follow the given word.        | No       |
| leads   | A word that tends to lead the given word.          | No       |

### `.suggestion_feedback`
Give manual feedback on the suggestions offered by the dictionary. This will increase the rating of the suggested word,
which can be found in the dictionary, the next time the incorrect word is given to find similar words for.

```python
# 'nor' is the incorrect spelling for 'not'
my_dictionary.suggestion_feedback('nor', 'not')
```

#### Parameters
| Name       | Description                                             | Required |
|------------|---------------------------------------------------------|----------|
| incorrect  | The word for which the suggestion was offered.          | Yes      |
| suggestion | The suggested word that can be found in the dictionary. | Yes      |

### `.unlearn`
Unlearn something the Dictionary knows. It is possible to unlearn a word by only providing a string of that word as the
first argument. If you want to unlearn something about a word, you should provide it as a string for the thing you want
to unlearn (see the details below). If the word wasn't found, a `LookupError` will be thrown.

```python
# To unlearn a word
my_dictionary.unlearn('foobar')

# To unlearn something about a word
my_dictionary.unlearn('foo', leads='bar')
```

#### Parameters
| Name     | Description                             | Required |
|----------|-----------------------------------------|----------|
| word     | The word to unlearn something about.    | Yes      |
| feedback | A piece feedback on the word to forget. | No       |
| follows  | A 'follows' word to forget.             | No       |
| leads    | A 'leads' word to forget.               | No       |

### `.export`
Export the AutoCorrect Dictionary to a file. If no file or path is given, a string of the serialized Dictionary will be
returned.

```python
my_dictionary.export(path='foobar.json')
```

#### Parameters
| Name     | Description                                                 | Required |
|----------|-------------------------------------------------------------|----------|
| file     | A file object of the file that should be imported.          | No       |
| path     | A string with the path to the file that should be imported. | No       |

* * *

# AutoCorrect.Import
Import an AutoCorrect Dictionary from a file or string and get a new Dictionary instance.

```python
import AutoCorrect
my_dictionary = AutoCorrect.Import(path='foobar.json')
```

#### Parameters
| Name   | Description                                               | Required |
|--------|-----------------------------------------------------------|----------|
| file   | A file object of the file that should be imported.        | Any      |
| path   | A string of the path to the file that should be imported. | Any      |
| string | A string of a serialized AutoCorrect Dictionary.          | Any      |
