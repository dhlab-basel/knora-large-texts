#!/usr/bin/env python3

import argparse
import re
import tempfile
from os import listdir
from os.path import isfile, join, splitext

import nltk
from knora import KnoraStandoffXml, Knora

pos_to_xml = {
    "NN": "noun",
    "NNP": "noun",
    "NNPS": "noun",
    "NNS": "noun",
    "VB": "verb",
    "VBD": "verb",
    "VBG": "verb",
    "VBN": "verb",
    "VBP": "verb",
    "VBZ": "verb",
    "JJ": "adj",
    "JJR": "adj",
    "JJS": "adj",
    "DT": "det"
}

replacements = {
    "<": "&lt;",
    ">": "&gt;"
}

title_regex = re.compile("^Title: (.*)$")
author_regex = re.compile("^Author: (.*)$")
sentence_length = 10
paragraph_length = 5


def make_fragments(lst, n):
    """Yield successive n-sized fragments from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def add_markup(input_file_path, output_file_base_path):
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

    tokens = nltk.word_tokenize(input_file_content)
    tagged = nltk.pos_tag(tokens)
    fragments = make_fragments(tagged, 1000)
    fragment_number = 0
    fragment_paths = []

    for fragment in fragments:
        output_file_path = output_file_base_path + "_" + str(fragment_number) + ".xml"
        fragment_paths.append(output_file_path)

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text>", file=output_file)
            sentence_count = 0
            word_count = 0

            for word, tag in fragment:
                escaped_word = word.replace("&", "&amp;")

                for replacement_in, replacement_out in replacements.items():
                    escaped_word = escaped_word.replace(replacement_in, replacement_out)

                if word_count == 0:
                    if sentence_count == 0:
                        output_file.write("<p>\n")

                    output_file.write("<sentence>")

                if tag == ".":
                    output_file.write(escaped_word)
                    output_file.write("\n")
                elif tag in pos_to_xml:
                    xml_label = pos_to_xml[tag]
                    output_file.write(f"<{xml_label}>{escaped_word}</{xml_label}> ")
                else:
                    output_file.write(escaped_word)
                    output_file.write(" ")

                word_count += 1

                if word_count == sentence_length:
                    output_file.write("</sentence>\n")
                    sentence_count += 1
                    word_count = 0

                if sentence_count == paragraph_length:
                    output_file.write("</p>\n")
                    sentence_count = 0

            if word_count > 0:
                output_file.write("</sentence>\n")
                sentence_count += 1

            if sentence_count > 0:
                output_file.write("</p>\n")

            print("</text>", file=output_file)
            fragment_number += 1

        print(f"Wrote {output_file_path}")

    return author, title, fragment_paths


def do_import(input_dir_path):
    temp_dir_path = tempfile.mkdtemp()
    print(f"Using temporary directory {temp_dir_path}")
    input_filenames = [file_path for file_path in listdir(input_dir_path)
                       if isfile(join(input_dir_path, file_path)) and file_path[len(file_path) - 4:] == ".txt"]

    con = Knora("http://0.0.0.0:3333")
    con.login("root@example.com", "test")
    schema = con.create_schema("00FD", "books")

    for input_filename in input_filenames:
        print(f"Processing {input_filename}...")
        input_filename_without_ext, _ = splitext(input_filename)
        input_file_path = join(input_dir_path, input_filename)
        output_file_base_path = join(temp_dir_path, f"{input_filename_without_ext}")
        author, title, fragment_paths = add_markup(input_file_path, output_file_base_path)
        fragment_number = 0
        fragment_iris = []

        for fragment_path in fragment_paths:
            with open(fragment_path, "r", encoding="utf-8") as xml_file:
                xml_content = xml_file.read()

                resource_info = con.create_resource(schema,
                                                    "BookFragment",
                                                    f"{input_filename_without_ext}_{fragment_number}", {
                                                        "seqnum": fragment_number,
                                                        "hasText": {
                                                            "value": KnoraStandoffXml(xml_content),
                                                            "mapping": "http://rdfh.ch/projects/00FD/mappings/LinguisticMapping"
                                                        }
                                                    })

                fragment_iri = resource_info['iri']
                print(f"Created BookFragment resource {fragment_iri}")
                fragment_iris.append(fragment_iri)
                fragment_number += 1

        resource_info = con.create_resource(schema, "Book", f"{input_filename_without_ext}", {
            "hasAuthor": author,
            "hasTitle": title,
            "hasFragment": fragment_iris
        })

        print(f"Created Book resource {resource_info['iri']}")


def main():
    parser = argparse.ArgumentParser(description="Imports Project Gutenberg books into Knora as fragments.")
    parser.add_argument("input", help="input directory")
    args = parser.parse_args()
    do_import(input_dir_path=args.input)


if __name__ == "__main__":
    main()
