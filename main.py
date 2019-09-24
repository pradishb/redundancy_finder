import argparse
import collections
import csv
import glob
import logging
import os
import re

import PIL
import pytesseract
import nltk

logging.getLogger().setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IGNORE = [
    "i", "ii", "iii", "iv",
    "a", "b", "c", "d", "e",
    "marks", "questions", "answers", "candidates", "fall", "spring",
    "pokhara", "notes", "university", "bachelor", "semester",
]


def is_valid_directory(parser, arg):
    if not os.path.exists(arg):
        parser.error("The directory %s does not exist!" % arg)
    return os.path.join(BASE_DIR, arg)


def arg_parser():
    parser = argparse.ArgumentParser(description="redundancy_finder")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-d", "--directory", required=True,
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

    for file in glob.glob(os.path.join(args["directory"], "*")):
        try:
            logging.info("Reading characters from %s", file)
            img = PIL.Image.open(file)
            word_list = word_list + word_list_from_img(img)
        except OSError:
            pass

    logging.info("Filtering the words using nltk")
    filtered_list = []
    tags = nltk.pos_tag(word_list)
    for tag in tags:
        if tag[1] in ("NN", "NNS"):
            filtered_list.append(tag[0])

    logging.info("Filtering the words in ignore list")
    filtered_list = [k for k in filtered_list if k not in IGNORE]

    logging.info("Couting the number of each words")
    counted_list = dict(collections.Counter(filtered_list))

    logging.info("Sorting the words")
    sorted_list = sorted(counted_list.items(), key=lambda kv: kv[1])

    logging.info("Writing to csv file")
    with open(args["output"], "w", newline='') as file:
        writer = csv.writer(file)
        for word in sorted_list:
            writer.writerow([word[0], word[1]])
