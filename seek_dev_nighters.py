import requests
import pytz
from datetime import datetime, timezone


def get_json_from_devman(page):
    url = 'https://devman.org/api/challenges/solution_attempts/'
    return requests.get(url, {'page': page}).json()


def get_user_data(json):
    for user in json['records']:
        user_timezone = pytz.timezone(user['timezone'])
        published_date = user_timezone.localize(
            datetime.fromtimestamp(user['timestamp']))
        user['published_date'] = published_date
        if published_date .hour >= 0 and published_date.hour < 7:
            user['is_night'] = True
        else:
            user['is_night'] = False
        yield user


def get_midnighters():
    midnighters = []
    first_page = 1
    pages = get_json_from_devman(first_page)["number_of_pages"]
    for page in range(1, pages+1):
        json = get_json_from_devman(page)
        for user in get_user_data(json):
            if user['is_night']:
                midnighters.append({'username': user['username'],
                                    'date': user['published_date']})
    return midnighters


if __name__ == '__main__':
    midnighters = get_midnighters()
    uniq_users = set([midnighter['username'] for midnighter in midnighters])
    print('There {} unique users, who send tasks at night'
          .format(len(uniq_users)))
    for user in uniq_users:
        print(user)
    print('These tasks are:')
    for midnighter in midnighters:
        print('User {} send task on {}'
              .format(midnighter['username'],
                      midnighter['date'].strftime("%H:%M %d.%m.%Y")))
