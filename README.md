# AutoCorrect
A Python module that provides a dictionary and a simple learning algorithm to
autocorrect words & texts.

* * *

## Getting started
To get started with this module you've got to create an AutoCorrect dictionary.
```python
import AutoCorrect
my_dictionary = AutoCorrect.Dictionary()
```

The first thing to do with a dictionary is learn it some words.
```python
# It can learn a single word.
my_dictionary.learn_word('foobar')

# Or it can learn from a piece of text.
my_dictionary.learn_text('Lorem ipsum dolor')
```

Once that is done, you can start using the dictionary to autocorrect words.
```python
# Oops, I typed 'foobar' incorrect.
mistake = 'fooabr'

# Lets see if my_dictionary can correct my mistake!
correction = my_dictionary.correct_word(mistake)
```

* * *

## General API
#### `.Dictionary()`
Create a new instance of the dictionary provided by this Python module.

```python
import AutoCorrect
my_dictionary = AutoCorrect.Dictionary()
```

#### `.Import()`
Import an AutoCorrect dictionary from a file (or string) and get a new
dictionary instance with the contents of the imported dictionary.

```python
import AutoCorrect
my_dictionary = AutoCorrect.Import(path='./foobar.json')
```

#### Parameters
| Name   | Description                                               | Required |
|--------|-----------------------------------------------------------|----------|
| file   | A file object of the file that should be imported.        | Any      |
| path   | A string of the path to the file that should be imported. | Any      |
| string | A string of a serialized AutoCorrect Dictionary.          | Any      |

#### Parameters
| Name     | Description                                                                   | Required |
|----------|-------------------------------------------------------------------------------|----------|
| alphabet | The alphabet that the Dictionary uses, this is a list of possible characters. | No       |

## Dictionary API
#### `.learn_text()`
Learn all the words from a string of text to the dictionary. This method expects
only one of the parameters to be provided.

```python
my_dictionary.learn_text(text='This sentence has some mistakes in it.') # (Well... it doesn't)
```

| Parameter | Required | Description |
|---|---|---|
| text | no | A string of the text to correct. |
| file | no | The file with the text to correct. |
| path | no | A string of the path to the file with the text to correct. |

#### `.learn_word()`
Learn a single word to the dictionary.

```python
my_dictionary.learn_word('foobar')
```

#### Parameters
| Parameter | Required | Description |
|---|---|---|
| word | yes | The word that should be learned by the dictionary. |
| follows | no | A word that tends to follow the given word. |
| leads | no | A word that tends to lead the given word. |

#### `.correct_text()`
Automatically correct a complete text based on the contents of the dictionary.
This will scan through the text and replace unknown words with the best
alternative it can find. This method expects only one of the parameters to be
provided.

```python
corrected_text = my_dictionary.correct_text(text='This setnence has some mitakes in it.')
print(corrected_text) # Gives 'This sentence has some mistakes in it.'
```

| Parameter | Required | Description |
|---|---|---|
| text | no | A string of the text to correct. |
| file | no | The file with the text to correct. |
| path | no | A string of the path to the file with the text to correct. |

#### `.correct_word()`
Automatically correct a single word based on the contents of the dictionary.

```python
corrected_word = my_dictionary.correct_word('fobar')
print(corrected_word) # Gives 'foobar'
```

| Parameter | Required | Description |
|---|---|---|
| word | yes | A string of the word to correct. |
| follows | no | A string of the word that is in front of `word`. |
| leads | no | A string of the word that comes after `word`. |

#### `.find_longer_words()`
Find all words in the dictionary that have a certain prefix. If no prefix is
provided this returns the complete dictionary.

```python
suggestions = my_dictionary.find_longer_words('foo')
print(suggestions) # Gives ['foobar']
```

| Parameter | Required | Description |
|---|---|---|
| prefix | no | A string with the prefix of choice. |

#### `.find_similar_words()`
Find all similar words for a given string known to the dictionary using a
combination of multiple different algorithms.

This method will return a list suggestions formatted in tuples of the following
structure: `(word, rating)`, ordered descending based on the rating.

```python
suggestions = my_dictionary.find_similar_words('fobar')
print(suggestions) # Suggests 'foobar'
```

| Parameter | Required | Description |
|---|---|---|
| word | yes | A string of the word to correct. |
| follows | no | A string of the word that is in front of `word`. |
| leads | no | A string of the word that comes after `word`. |

#### `.find_word()`
Find a word in the dictionary and get a tuple with some information about it.

```python
word = my_dictionary.find_word('foobar')
print(word) # Gives a tuple with information about 'foobar'
```

| Parameter | Required | Description |
|---|---|---|
| word | yes | A string of the word to correct. |

#### `.get_dictionary()`
Get all the words known to the dictionary.

```python
dictionary = my_dictionary.get_dictionary()
print(dictionary) # Gives a list of all the words in the dictionary
```

#### `.suggestion_feedback()`
Give manual feedback on the suggestions offered by the dictionary. This will
increase the rating of the suggested word the next time the dictionary is asked
to correct the incorrect word.

```python
my_dictionary.suggestion_feedback('nol', 'not')
```

#### Parameters
| Parameter | Required | Description |
|---|---|---|
| incorrect | yes | The word for which the suggestion was offered. |
| suggestion | yes | The suggested word that can be found in the dictionary. |

### `.unlearn`
Unlearn something the Dictionary knows. It is possible to unlearn a word by only
providing a string of that word as the first argument. If the word wasn't found,
a `LookupError` will be thrown.

If you want to unlearn something specific about a word, you should provide it as
a string for the thing you want to unlearn (for the details, see below).

```python
# To unlearn a word
my_dictionary.unlearn('foobar')

# To unlearn something about a word
my_dictionary.unlearn('foo', leads='bar')
```

#### Parameters
| Parameter | Required | Description |
|---|---|---|
| word | yes | The word to unlearn (something about). |
| feedback | no | A piece feedback on the word to forget. |
| follows | no | A word the dictionary expects in front of `word` to forget. |
| leads | no | A word the dictionary expects after `word` to forget. |

#### `.export()`
Export the dictionary to a file so it can be imported at a later point in time.

```python
my_dictionary.export(path='./foobar.json')
```

| Parameter | Required | Description |
|---|---|---|
| file | no | The file to write the dictionary to. |
| path | no | A string of the path to the file to write the dictionary to. |

* * *

## Testing
In order to run the tests for this module use the command:
```
$ python -m unittest discover
```

* * *

Copyright © 2016-2017 Eric Cornelissen | MIT license
