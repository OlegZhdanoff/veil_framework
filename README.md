# Veil Framework
simple MVC framework

Run test server from `python run.py` with wsgiref.simple_server if `DEBUG = True` in settings.py

## How to start on Ubuntu:
######First you need to install python3, uwsgi:
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install python-pip
    pip install uwsgi
######Run example:
    uwsgi --http :8000 --wsgi-file run.py

    