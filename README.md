# knora-large-texts

Testing performance of Knora with large texts.

Requires:

- [knora-py](https://github.com/dasch-swiss/knora-py)
- [NLTK](https://www.nltk.org)
- [Requests](https://requests.kennethreitz.org/en/master/)

## Creating the Repository

1. Start GraphDB.

2. Create the `knora-test` repository using `knora-api/webapi/scripts/graphdb-se-local-init-knora-test.sh`.

3. Delete the Redis cache: `rm dump.rdb`.

3. Start Redis, Sipi, and Knora.

4. Run `knora-create-ontology book-onto.json`.

5. Stop Knora.

6. Run `./upload-standoff-defs.sh`.

7. Start Knora.

8. Run `./send-mapping.py`.

9. Run `./import.py INPUT`, where `INPUT` is a directory containing plain-text versions of books
   downloaded from [Project Gutenberg](https://www.gutenberg.org).

## Generated Markup

The text is run through the NLTK POS tagger to add
(where `WORD` is the word being marked up):

- `<noun word="WORD">WORD</noun>` (`books:StandoffNounTag`) for nouns
- `<verb word="WORD">WORD</verb>` (`books:StandoffVerbTag`) for verbs
- `<adj word="WORD">WORD</adj>` (`books:StandoffAdjectiveTag`) for adjectives
- `<det word="WORD">WORD</det>` (`books:StandoffDeterminerTag`) for determiners

Each group of ten words is wrapped in `<sentence>` (`books:StandoffSentenceTag`).

Each group of five `<sentence>` elements is wrapped in `<p>` (`standoff:StandoffParagraphTag`).
