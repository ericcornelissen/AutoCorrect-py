# AutoCorrect
A Python module that provides a dictionary and a simple learning algorithm to autocorrect texts.

* * *

## Getting started
To get started with this module you've got to create an AutoCorrect dictionary.
```python
import AutoCorrect
my_dictionary = AutoCorrect.dictionary()
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
word = 'fooabr'

# Lets see if my_dictionary can correct my mistake!
my_dictionary.find_similar_words(word)
```

* * *

## Tests
In order to run the unittests for this module, it is required that you install it as a package. This can be done by
running the following command from the root of the project.
```
$ python setup.py install
```

Once that is done, all tests can be run using the command:
```
$ python -m unittest discover
```

* * *

Copyright © 2016 Eric Cornelissen | MIT license
