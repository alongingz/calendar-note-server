from flask import Flask
from gevent import pywsgi

from config import default_port, default_ip
from src.pub_calendar import pub_calendar

app = Flask(__name__)
app.secret_key = 'nishiwodexiaoyaxiaopingguo'
app.register_blueprint(blueprint=pub_calendar)

if __name__ == '__main__':
    server = pywsgi.WSGIServer((default_ip, default_port), application=app)
    server.serve_forever()
