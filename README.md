# knora-large-texts

Testing performance of Knora with large texts.

The program `import.py` takes a directory of plain-text files downloaded
from [Project Gutenberg](https://www.gutenberg.org), adds markup to them,
and uploads them to Knora using [knora-py](https://github.com/dasch-swiss/knora-py).

The added markup is as follows:

- The text is run through the [NLTK](https://www.nltk.org) POS tagger to add:

  - `<em>` (`StandoffItalicTag`) for nouns
  - `<strong>` (`StandoffBoldTag`) for verbs
  - `<u>` (`StandoffUnderlineTag`) for adjectives
  - `<strike>` (`StandoffStrikethroughTag`) for determiners

- Each group of ten words is wrapped in `<li>` (`StandoffListElementTag`).

- Each group of five `<li>` elements is wrapped in `<ol>` (`StandoffOrderedListTag`).
