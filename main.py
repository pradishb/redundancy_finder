from PIL import Image
import pytesseract
import re
from collections import Counter


if __name__ == "__main__":
    text = pytesseract.image_to_string(Image.open('test.jpg'))
    word_list = re.sub(r"[^\w]", " ", text).split()
    a = dict(Counter(word_list))
    print(a)
