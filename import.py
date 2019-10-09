#!/usr/bin/env python3

import argparse
import nltk
import re


pos_to_xml = {
    "NN": "em",
    "NNP": "em",
    "NNPS": "em",
    "NNS": "em",
    "VB": "strong",
    "VBD": "strong",
    "VBG": "strong",
    "VBN": "strong",
    "VBP": "strong",
    "VBZ": "strong",
    "JJ": "u",
    "JJR": "u",
    "JJS": "u",
    "DT": "strike"
}


title_regex = re.compile("^Title: (.*)$")
author_regex = re.compile("^Author: (.*)$")
sentence_length = 10
paragraph_length = 5


def add_markup(input_file_path, output_file_path):
    title = None
    author = None

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        got_metadata = False

        while not got_metadata:
            line = input_file.readline()
            title_match = title_regex.match(line)

            if title_match is not None:
                title = title_match.group(1)
            else:
                author_match = author_regex.match(line)

                if author_match is not None:
                    author = author_match.group(1)
                elif line[0:3] == "***":
                    got_metadata = True

        input_file_content = input_file.read()

    print(f"Title: {title}")
    print(f"Author: {author}")

    tokens = nltk.word_tokenize(input_file_content)
    tagged = nltk.pos_tag(tokens)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text>", file=output_file)
        sentence_count = 0
        word_count = 0

        for word, tag in tagged:
            if word_count == 0:
                if sentence_count == 0:
                    output_file.write("<ol>\n")

                output_file.write("<li>")

            if tag == ".":
                output_file.write(word)
                output_file.write("\n")
            elif tag in pos_to_xml:
                xml_label = pos_to_xml[tag]
                output_file.write(f"<{xml_label}>{word}</{xml_label}> ")
            else:
                output_file.write(word)
                output_file.write(" ")

            word_count += 1

            if word_count == sentence_length:
                output_file.write("</li>\n")
                sentence_count += 1
                word_count = 0

            if sentence_count == paragraph_length:
                output_file.write("</ol>\n")
                sentence_count = 0

        if word_count > 0:
            output_file.write("</li>\n")
            sentence_count += 1

        if sentence_count > 0:
            output_file.write("</ol>\n")

        print("</text>", file=output_file)


def main():
    parser = argparse.ArgumentParser(description="Imports Project Gutenberg books into Knora, adding markup.")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    args = parser.parse_args()
    add_markup(input_file_path=args.input, output_file_path=args.output)


if __name__ == "__main__":
    main()
