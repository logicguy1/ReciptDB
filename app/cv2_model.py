import cv2
from PIL import Image, ImageEnhance
from tesserocr import PyTessBaseAPI
import chardet
import uuid
import os
import threading
import numpy as np

from app import app

import locale
locale.setlocale(locale.LC_ALL, "C")


def worker(img_gs, i, wordlist, images, dim):
    print("Started working", i)
    # Perform binary thresholding on the image with T = 125
    if i > 0:
        r, threshold = cv2.threshold(img_gs, i, 255, cv2.THRESH_BINARY)
        img = threshold
    else:
        img = img_gs

    # Get OCR data
    with PyTessBaseAPI(path="/usr/share/tessdata/tessdata", lang='dan') as api:
        pil_img = Image.fromarray(img)
        api.SetImage(pil_img)
        text = api.GetUTF8Text()
        confidence = api.AllWordConfidences()
        #text = [i for i, c in zip(text.split(" "), confidence) if c > 0]
        text = "\n".join([i for i in text.split("\n") if len(i) > 2 or i.strip() == ""])
        
    # resize image
    resized = cv2.resize(img_gs, dim, interpolation = cv2.INTER_AREA)
    
    # Define the images score
    score = len([i for i in text.split(" ") \
                 if i.strip().lower() in wordlist or \
                 i.strip().replace(",", "").replace(".", "").isdigit()])
    images[i] = {
            "image": resized,
            "score": score,
            "text": text
        }

    print("Stopping thread", i, "with a score of", score)


def process_image(file_name):
    images = {}

    with open(f"app/assets/{app.config['WORDLIST']}", "r", encoding="charmap") as file:
        wordlist = [i.strip().split("/")[0].lower() for i in file.readlines()]
        print(wordlist)

    # The sentensivity of the filter
    large = [0, 50, 80, 100, 120, 140, 160]
    large = list(range(0, 50, 20)) + list(range(50, 150, 10)) + list(range(150, 255, 50))
    small = [100,]

    # Read image as grayscale
    img_gs = cv2.imread(f'app/assets/recipts/{file_name}', cv2.IMREAD_GRAYSCALE)
    img_enhanced = Image.fromarray(img_gs)
    img_enhanced = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = img_enhanced.enhance(0.5)
    img_enhanced = np.array(img_enhanced)

    # Calculate new size params
    scale_percent = 450 / img_gs.shape[1] # percent of original size
    width = int(img_gs.shape[1] * scale_percent)
    height = int(img_gs.shape[0] * scale_percent)
    dim = (width, height)
      
    # Print image props
    print("Image Properties")
    print("- Number of Pixels: " + str(img_gs.size))
    print("- Shape/Dimensions: " + str(img_gs.shape))

    threads = []
    for i in large:
        thread = threading.Thread(target=worker, args=(img_enhanced, i, wordlist, images, dim))
        thread.start()
        threads.append(thread)

    running = True
    while running:
        running = False
        for thread in threads:
            running = thread.is_alive() if not running else running

    key, data = max(images.items(), key=lambda k: k[1]["score"])

    r, threshold = cv2.threshold(data["image"], key, 255, cv2.THRESH_BINARY)

    img = cv2.imread(f'app/assets/recipts/{file_name}')
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    """if app.config["DEBUG"] == True:
        print(data["text"])
        print(data["score"])
        cv2.imshow("img", img)
        while True:
            key = cv2.waitKey(0)
            if key == 27:
                break
         
        # closing all open windows
        cv2.destroyAllWindows()"""

    os.remove(f'app/assets/recipts/{file_name}') 
    name = str(uuid.uuid4())+"."+file_name.split(".")[-1]
    im = Image.fromarray(img_gs)
    im.save(f"app/assets/recipts/{name}")

    return data["text"], name


