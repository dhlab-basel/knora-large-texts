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

        for word, tag in tagged:
            if tag == ".":
                output_file.write(word)
                output_file.write("\n")
            elif tag in pos_to_xml:
                xml_label = pos_to_xml[tag]
                output_file.write(f"<{xml_label}>{word}</{xml_label}> ")
            else:
                output_file.write(word)
                output_file.write(" ")

        print("</text>", file=output_file)


def main():
    parser = argparse.ArgumentParser(description="Adds markup to text.")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    args = parser.parse_args()
    add_markup(input_file_path=args.input, output_file_path=args.output)


if __name__ == "__main__":
    main()
