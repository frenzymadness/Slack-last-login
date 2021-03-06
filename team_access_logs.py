#!/usr/bin/env python3

import csv
from time import sleep
from datetime import datetime

from api_token import token

import requests
from tqdm import trange


def write_dicts_to_csv(filename, dictionaries):
    field_names = dictionaries[0].keys()
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for dictionary in dictionaries:
            writer.writerow(dictionary)


def get_access_logs():
    all_access_logs = []
    url = 'https://slack.com/api/team.accessLogs'
    params = {'token': token, 'count': 1000}  # 1000 logs per page is maximum

    print(' Downloading pages …')
    for page in trange(1, 101):  # 100 pages is maximum
        params['page'] = page
        res = requests.get(url, params=params)
        res_data = res.json()

        if not res_data['ok']:
            raise ValueError(f'Something went wrong.'
                             'URL: {res.url}'
                             'Error: {res_data["error"]}')

        all_access_logs.extend(res_data['logins'])

        sleep(3)  # Limit for Tier 2 is 20 req/min

    return all_access_logs


def get_last_logins(access_logs):
    last_logins = {}  # {user_id: last_login}
    user_names = {}  # {user_id: user_name}
    user_dicts = []  # all info ready for write to csv
    for log in access_logs:
        user_id = log['user_id']
        user_name = log['username']
        last_login = log['date_last']
        if user_id not in last_logins:
            last_logins[user_id] = last_login
        else:
            if last_login > last_logins[user_id]:
                last_logins[user_id] = last_login

        user_names[user_id] = user_name

    for user_id, user_name in user_names.items():
        now = datetime.now()
        last_login_dtm = datetime.fromtimestamp(last_logins[user_id])
        inactive = now - last_login_dtm
        inactive_days = inactive.days
        user_dicts.append({
            'user_id': user_id,
            'user_name': user_name,
            'last_login': last_login_dtm.isoformat(),
            'inactive_days': inactive_days})

    return user_dicts


def get_all_members():
    url = 'https://slack.com/api/users.list'
    params = {'token': token}  # 1000 logs per page is maximum

    print(' Downloading members …')
    res = requests.get(url, params=params)
    res_data = res.json()

    if not res_data['ok']:
        raise ValueError(f'Something went wrong.'
                            'URL: {res.url}'
                            'Error: {res_data["error"]}')

    return res_data["members"]


def add_missing_members(last_logins, all_members):
    """Extends info about last logins with members missing in access logs"""
    existing_ids = [user["user_id"] for user in last_logins]

    for member in all_members:
        if member["id"] in existing_ids:
            continue
        last_logins.append({
            'user_id': member["id"],
            'user_name': member["name"],
            'last_login': "Not available",
            'inactive_days': "Not available"})


def main():
    access_logs = get_access_logs()
    write_dicts_to_csv('raw_data.csv', access_logs)
    last_logins = get_last_logins(access_logs)
    members = get_all_members()
    add_missing_members(last_logins, members)
    write_dicts_to_csv('last_logins.csv', last_logins)


if __name__ == '__main__':
    main()
