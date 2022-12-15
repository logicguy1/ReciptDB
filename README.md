# ReciptDB
Your personal recipt database and management software



## Roadmap

- [ ] Fix design for mobile
- [ ] Share button to share a recipt without having to login
  - [x] Core system
  - [ ] Comments
- [ ] Edit tags
- [ ] Minimise sidebar
- [ ] Statistics for model, usefull for optimisations
- [ ] Error menu


## Installation

Download CV2 training data
```sh
$ mkdir /usr/share/tessdata
$ cd /usr/share/tessdata
$ git clone https://github.com/tesseract-ocr/tessdata_fast
```

Install requred software
```sh
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install postfix nginx git tesseract-ocr
```

### Python venv
The virtualenvirunniment
```sh
$ python3.9 -m venv venv
$ source venv/bin/activate
(venv) $ python3.9 -m pip install -r requirements.txt
```

Create `.env` file
```sh
SECRET_KEY=<app secret key>
SQLALCHEMY_DATABASE_URI=sqlite:///home/ubuntu/ReciptDB/app/app.db
```


### NGRIX
Create self signed certs
```sh
# Within the project files
$ mkdir certs
$ openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem
```

Remove default config
```sh
$ rm /etc/nginx/sites-enabled/default
```

Server config located in the file at `/etc/nginx/sites-enabled/ReciptDB`
```sh
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /home/ubuntu/ReciptDB/certs/cert.pem;
    ssl_certificate_key /home/ubuntu/ReciptDB/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/ReciptDB_access.log;
    error_log /var/log/ReciptDB_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/ubuntu/ReciptDB/app/static;
        expires 30d;
    }
}

```

Reload NGINX server
```sh
service nginx reload
```

Running the server
```sh
# We set timeout so that when we load the CV2 models we dont crash
/home/ubuntu/ReciptDB/venv/bin/gunicorn -b localhost:8000 -w 4 --timeout 600 ReciptDB:app
```
