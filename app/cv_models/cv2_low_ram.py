import cv2
from PIL import Image, ImageEnhance
from tesserocr import PyTessBaseAPI
import chardet
import uuid
import os
import threading
import numpy as np
import time

from app import app

import locale
locale.setlocale(locale.LC_ALL, "C")


def worker(img_gs, i, images, dim):
    print("[THREAD] Starting", i)
    # Perform binary thresholding on the image with T = 125
    if i > 0:
        r, threshold = cv2.threshold(img_gs, i, 255, cv2.THRESH_BINARY)
        img = threshold
    else:
        img = img_gs

    # Get OCR data
    try:
        with PyTessBaseAPI(path="/usr/share/tessdata/tessdata", lang='dan') as api:
            pil_img = Image.fromarray(img)
            api.SetImage(pil_img)
            text = api.GetUTF8Text()
            confidence = api.AllWordConfidences()
            #text = [i for i, c in zip(text.split(" "), confidence) if c > 0]
            text = "\n".join([i for i in text.split("\n") if len(i) > 2 or i.strip() == ""])
    except Exception as err:
        print(f"[Thread] FAILED {err}, TERMINATING")
        return
        
    # resize image
    resized = cv2.resize(img_gs, dim, interpolation = cv2.INTER_AREA)
    
    # Define the images score
    score = len([i for i in text.split(" ") \
                 if i.strip().replace(",", "").replace(".", "").isdigit() or \
                 len(i.strip()) > 4    
            ])

    images[i] = {
            "score": score,
            "text": text
        }

    print("[THREAD] COMPLRETE", i, "with a score of", score)


def process_image(file_name):
    images = {}

    # The sentensivity of the filter
    verylarge = list(range(0, 50, 20)) + list(range(50, 150, 10)) + list(range(150, 255, 50))
    large = [0, 50, 80, 100, 120, 140, 160]
    medium = list(range(100, 150, 15)) + [200]
    quite_small = [125]
    small = [100,]

    # Read image as grayscale
    print("Reading uploaded image")
    img_gs = cv2.imread(f'app/assets/uploads/{file_name}', cv2.IMREAD_GRAYSCALE)
    img_enhanced = Image.fromarray(img_gs)
    img_enhanced = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = img_enhanced.enhance(0.5)
    img_enhanced = np.array(img_enhanced)

    # Calculate new size params
    print("Calculating scaleing")
    scale_percent = 450 / img_gs.shape[1] # percent of original size
    width = int(img_gs.shape[1] * scale_percent)
    height = int(img_gs.shape[0] * scale_percent)
    dim = (width, height)
    img_gs = cv2.resize(img_gs, dim, interpolation = cv2.INTER_AREA)
      
    # Print image props
    print("Image Properties")
    print("- Number of Pixels: " + str(img_gs.size))
    print("- Shape/Dimensions: " + str(img_gs.shape))

    for i in medium:
        worker(img_enhanced, i, images, dim)

    key, data = max(images.items(), key=lambda k: k[1]["score"])

    os.remove(f'app/assets/uploads/{file_name}') 
    name = str(uuid.uuid4())+"."+file_name.split(".")[-1]
    im = Image.fromarray(img_gs)
    im.save(f"app/assets/recipts/{name}")

    return data["text"].strip(), name



