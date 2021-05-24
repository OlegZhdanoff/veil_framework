from create_db import create_db
from veil_framework.main import Framework
from urls import fronts
from wsgiref.simple_server import make_server

from veil_framework.settings import DEBUG
from views import routes

application = Framework(routes, fronts)

if DEBUG:
    # create_db()
    with make_server('', 8080, application) as httpd:
        print("Run server at port 8080...")
        httpd.serve_forever()
