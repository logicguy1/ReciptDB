
import cv2
from PIL import Image
from tesserocr import PyTessBaseAPI

import locale
locale.setlocale(locale.LC_ALL, "C")

# Read image as grayscale
img_gs = cv2.imread('recipts/IMG_4212.jpg', cv2.IMREAD_GRAYSCALE)

# Print image props
print("Image Properties")
print("- Number of Pixels: " + str(img_gs.size))
print("- Shape/Dimensions: " + str(img_gs.shape))

# Perform binary thresholding on the image with T = 125
r, threshold = cv2.threshold(img_gs, 160, 255, cv2.THRESH_BINARY)
img = threshold

# Get OCR data
with PyTessBaseAPI(path="/usr/share/tessdata/tessdata", lang='dan') as api:
    pil_img = Image.fromarray(img)
    api.SetImage(pil_img)
    text = api.GetUTF8Text()
    confidence = api.AllWordConfidences()
    print(text)
    print(confidence)
    #text = [i for i, c in zip(text.split(" "), confidence) if c > 0]
    text = "\n".join([i for i in text.split("\n") if len(i) > 5 or i == "\n"])
    print(text)
    
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(threshold, dim, interpolation = cv2.INTER_AREA)

# cv2.imshow("img", img)
cv2.imshow("img", resized)
while True:
    key = cv2.waitKey(0)
    if key == 27:
        break
 
# closing all open windows
cv2.destroyAllWindows()

