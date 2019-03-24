import argparse
import collections
import glob
import os
import re
import logging

import PIL
import pytesseract

logging.getLogger().setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IGNORE = ["the", "of", "a", "b", "c", "d", "e", "f", "and", "is", "s",
          "in",  "to", "what", "write", "explain", "discuss", "user", "each", "for", "by", "are", "an", "that", "calculate", "as", "marks", "has", "show", "any", "i", "give"]


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


def word_list_from_img(img):
    text = pytesseract.image_to_string(img)
    lowered_text = text.lower()
    word_list = re.sub(r"[^\w]", " ", lowered_text).split()
    return word_list


if __name__ == "__main__":
    args = arg_parser()
    word_list = []

    for file in glob.glob(args["directory"] + "\\*"):
        logging.info("Reading characters from file %s", file)
        img = PIL.Image.open(file)
        word_list = word_list + word_list_from_img(img)

    counted_list = dict(collections.Counter(word_list))
    filtered_list = {k: v for k, v in counted_list.items()
                     if k not in IGNORE}

    sorted_list = sorted(filtered_list.items(), key=lambda kv: kv[1])
    print(sorted_list)
