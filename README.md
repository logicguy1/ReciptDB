# ReciptDB
Your personal recipt database and management software


Download CV2 training data
```
$ mkdir /usr/share/tessdata
$ cd /usr/share/tessdata
$ git clone https://github.com/tesseract-ocr/tessdata
```

Reload NGRIX server
```
service nginx reload
```

Running the server
```sh
# We set timeout so that when we load the CV2 models we dont crash
/home/ubuntu/ReciptDB/venv/bin/gunicorn -b localhost:8000 -w 4 --timeout 600 ReciptDB:app
```
