from flask import Flask
from gevent import pywsgi

from src.pub_calendar import pub_calendar

app = Flask(__name__)
app.secret_key = 'nihsiwodexiaoyaxiaopingguo'
app.register_blueprint(blueprint=pub_calendar)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("0.0.0.0", 5000), application=app)
    server.serve_forever()
