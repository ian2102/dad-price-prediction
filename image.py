import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def remove_identical_parts(base_image_path, new_image_obj, threshold_value=10):
    base_image_obj = Image.open(base_image_path)

    base_image = np.array(base_image_obj)
    new_image = np.array(new_image_obj)

    base_gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(base_gray, new_gray)

    _, thresh = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    new_image[thresh == 0] = 0

    result_image = Image.fromarray(new_image)

    return result_image

def image_to_text(screenshot):
    text = pytesseract.image_to_string(screenshot)
    return text

def file_to_image(file):
    image = Image.open(io.BytesIO(file.read()))
    return image

def text_correction(text):
    return text

if __name__ == "__main__":
    with open ("data/data5.txt", "r") as file:
        lines = file.readlines()

    line = lines[1]
    print(line)
    line = line.replace("\\n", " ")
    cleaned_line = re.sub(r"[^a-zA-Z0-9 .]", "", line)
    print(cleaned_line)