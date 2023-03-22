import json
from random import randint

import requests

BASE_URL = 'http://localhost:8080/api'


def main_job() -> None:
    test_all_jobs()
    test_one_job()
    test_not_exist_job()
    test_id_str_job()


def test_all_jobs() -> None:
    response = requests.get(f'{BASE_URL}/jobs')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_one_job() -> None:
    response = requests.get(f'{BASE_URL}/jobs/1')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_not_exist_job() -> None:
    response = requests.get(f'{BASE_URL}/jobs/500')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_id_str_job() -> None:
    response = requests.get(f'{BASE_URL}/jobs/qwert')
    print(response.status_code)


def test_add_job() -> None:
    response = requests.post(f'{BASE_URL}/jobs', json={
        'id': randint(1000, 10000),
        'job': 'installation of radiation protection',
        'team_leader': 1,
        'work_size': 45,
        'collaborators': '6, 4, 7',
        'is_finished': False,
    })
    data = response.json()
    print(json.dumps(data, indent=4))
    test_all_jobs()


def test_add_job_already_exists() -> None:
    response = requests.post(f'{BASE_URL}/jobs', json={
        'id': 1,
        'job': 'installation of radiation protection',
        'team_leader': 1,
        'work_size': 45,
        'collaborators': '6, 4, 7',
        'is_finished': False,
    })
    data = response.json()
    print(json.dumps(data, indent=4))
    test_all_jobs()
