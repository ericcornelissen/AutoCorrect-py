# AutoCorrect
A Python module that provides a dictionary and a simple learning algorithm to autocorrect words & texts.

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
my_dictionary.find_similar_words(mistake)
```

* * *

## Testing
In order to run the tests for this module use the command:
```
$ python -m unittest discover
```

* * *

Copyright © 2016 Eric Cornelissen | MIT license
