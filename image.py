import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
from datetime import datetime
import os
from PIL import ImageGrab

# adjust as needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ["TESSDATA_PREFIX"] = r"models\tesseract"

def image_to_text(screenshot):
    text = pytesseract.image_to_string(screenshot)
    return text

def file_to_image(file):
    image = Image.open(io.BytesIO(file.read()))
    return image

def save_image(image, img_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    data_file_name = f"{timestamp}.png"
    file_path = os.path.join(img_dir, data_file_name)
    cv2.imwrite(file_path, image)
    return file_path

def screenshot():
    img_pil = ImageGrab.grab()
    img_np = np.array(img_pil)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_np
