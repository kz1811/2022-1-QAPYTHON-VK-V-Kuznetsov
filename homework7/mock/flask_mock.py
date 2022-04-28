#!/usr/bin/env python3.10

import threading
import json
from flask import Flask, jsonify, request

import settings

app = Flask(__name__)


SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if SURNAME_DATA.get(name) is not None:
        return jsonify(SURNAME_DATA.get(name)), 200
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


@app.route('/set_surname', methods=['PUT'])
def set_user_surname():

    name = json.loads(request.data)['name']
    surname = json.loads(request.data)['surname']

    SURNAME_DATA[name] = surname
    # return jsonify(surname), 200
    return 204


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        del SURNAME_DATA[name]
        return 204
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    return server
