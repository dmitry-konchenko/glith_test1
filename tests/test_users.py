import json
from random import randint

import requests

BASE_URL = 'http://localhost:8080/api/v2'


def main_users() -> None:
    test_all_users()
    test_one_user()
    test_not_exist_user()
    test_add_user()
    test_delete_user()


def test_all_users() -> None:
    response = requests.get(f'{BASE_URL}/users')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_one_user() -> None:
    response = requests.get(f'{BASE_URL}/users/1')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_not_exist_user() -> None:
    response = requests.get(f'{BASE_URL}/users/500')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_delete_user() -> None:
    response = requests.delete(f'{BASE_URL}/users/3508')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_add_user() -> None:
    response = requests.post(f'{BASE_URL}/users', json={
        'id': 2,
        'surname': 'Pirat',
        'name': 'Serega',
        'age': 28,
        'position': 'carry',
        'speciality': 'clown',
        'address': 'easy_lane',
        'email': 'radik1@mail.com',
        'password': 'yaneotmenaltp123',

    })
    data = response.json()
    print(json.dumps(data, indent=4))
    test_all_users()
