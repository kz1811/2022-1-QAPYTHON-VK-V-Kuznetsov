#!/usr/bin/env python3.9

import json
import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_DATA = {}
USER_ID_SEQ = 1


@app.route('/add_user', methods=['POST'])
def create_user():
    global USER_ID_SEQ

    user_name = json.loads(request.data)['name']
    if user_name not in APP_DATA:
        APP_DATA[user_name] = USER_ID_SEQ
        USER_ID_SEQ += 1

        return jsonify({'user_id': APP_DATA[user_name]}), 201

    else:
        return jsonify(f'User_name {user_name} already exists: id: {APP_DATA[user_name]}'), 400


@app.route('/get_user/<name>', methods=['GET'])
def get_user(name):
    if user_id := APP_DATA.get(name):
        age_host = os.environ['AGE_HOST']
        age_port = os.environ['AGE_PORT']

        # get age from external system 1
        age = None
        try:
            age = requests.get(f'http://{age_host}:{age_port}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system 1:\n{e}')

        # get surname from external system 2
        surname_host = os.environ['SURNAME_HOST']
        surname_port = os.environ['SURNAME_PORT']

        surname = None
        try:
            response = requests.get(f'http://{surname_host}:{surname_port}/get_surname/{name}')
            if response.status_code == 200:
                surname = response.json()
            else:
                print(f'No surname found for user {name}')
        except Exception as e:
            print(f'Unable to get surname from external system 2:\n{e}')

        data = {'user_id': user_id,
                'age': age,
                'surname': surname
                }

        return jsonify(data), 200
    else:
        return jsonify(f'User_name {name} not found'), 404


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    user_name = json.loads(request.data)['name']

    if user_name in APP_DATA:
        del APP_DATA[user_name]

        surname_host = os.environ['SURNAME_HOST']
        surname_port = os.environ['SURNAME_PORT']

        try:
            response = requests.get(f'http://{surname_host}:{surname_port}/delete_surname/{user_name}')
            if response.status_code != 204:
                print(f'No surname found for user {user_name}')
        except Exception as e:
            print(f'Unable to get surname from external system 2:\n{e}')

        return jsonify(f"user {user_name} was succesfully deleted"), 200
    else:
        return jsonify(f'User_name {user_name} not found'), 404


@app.route('/change_user', methods=['PUT'])
def change_user_data():
    name = json.loads(request.data)['name']
    surname = json.loads(request.data)['surname']
    if name in APP_DATA:

        surname_host = os.environ['SURNAME_HOST']
        surname_port = os.environ['SURNAME_PORT']

        json_data = {'name': name, 'surname': surname}
        try:
            response = requests.put(f'http://{surname_host}:{surname_port}/set_surname', json=json_data)
            if response.status_code != 204:
                print(f'No surname found for user {name}')
        except Exception as e:
            print(f'Unable to get surname from external system 2:\n{e}')
        return jsonify(f"Data for user {name} {surname} was succesfully changed"), 200
    else:
        return jsonify(f'User_name {name} not found'), 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '4444')
    app.run(host, port)
