import argparse
import collections
import glob
import os
import re

import PIL
import pytesseract

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IGNORE = ["the", "of", "a", "b", "c", "d", "e", "f", "and", "is", "s",
          "in",  "to", "what", "write", "explain", "discuss", "user", "each"]


def is_valid_directory(parser, arg):
    if not os.path.exists(arg):
        parser.error("The directory %s does not exist!" % arg)
    return os.path.join(BASE_DIR, arg)


def arg_parser():
    parser = argparse.ArgumentParser(description="redundancy_finder")
    parser.add_argument("-d", dest="directory", required=True,
                        help="directory to images",
                        type=lambda x: is_valid_directory(parser, x))
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = arg_parser()

    text = pytesseract.image_to_string(PIL.Image.open('test.jpg'))
    lowered_text = text.lower()
    word_list = re.sub(r"[^\w]", " ", lowered_text).split()
    counted_list = dict(collections.Counter(word_list))
    filtered_list = {k: v for k, v in counted_list.items()
                     if k not in IGNORE}

    sorted_list = sorted(filtered_list.items(), key=lambda kv: kv[1])
    print(sorted_list)
