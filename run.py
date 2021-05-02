from veil_framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server

from veil_framework.settings import DEBUG

application = Framework(routes, fronts)

if DEBUG:
    with make_server('', 8080, application) as httpd:
        print("Run server at port 8080...")
        httpd.serve_forever()
