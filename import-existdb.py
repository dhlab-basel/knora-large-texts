#!/usr/bin/env python3

import argparse
from os import listdir
from os.path import isfile, join, splitext
import requests


def do_import(input_dir_path):
    input_filenames = [file_path for file_path in listdir(input_dir_path)
                       if isfile(join(input_dir_path, file_path)) and file_path[len(file_path) - 4:] == ".xml"]

    for input_filename in input_filenames:
        print(f"Processing {input_filename}...")
        input_filename_without_ext, _ = splitext(input_filename)
        input_file_path = join(input_dir_path, input_filename)

        with open(input_file_path, "r", encoding="utf-8") as xml_file:
            xml_content = xml_file.read()
            content_length = len(xml_content)
            url = f"http://localhost:9090/exist/rest/db/books/{input_filename_without_ext}"
            auth = ("admin", "")
            headers = {
                "Content-Type": "application/xml",
                "Content-Length": str(content_length)
            }
            r = requests.put(url, headers=headers, auth=auth, data=xml_content)
            r.raise_for_status()
            break


def main():
    parser = argparse.ArgumentParser(description="Imports XML files into eXist-db.")
    parser.add_argument("input", help="input directory")
    args = parser.parse_args()
    do_import(input_dir_path=args.input)


if __name__ == "__main__":
    main()
