import logging

from flask import Flask
from flask import request

from client import instance as qq_client

app = Flask(__name__)

logging.disable(logging.ERROR)


def start_server():
    app.run("127.0.0.1", 5000)


@app.route('/client', methods=["POST"])
def client():
    event_json: dict = request.json
    qq_client.handle(event_json)
    return " "


if __name__ == '__main__':
    start_server()
