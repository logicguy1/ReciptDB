from tesserocr import PyTessBaseAPI

import locale
locale.setlocale(locale.LC_ALL, "C")


images = ['recipts/IMG_4210.jpg']

with PyTessBaseAPI(path="/usr/share/tessdata/tessdata") as api:
    for img in images:
        api.SetImageFile(img)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.
