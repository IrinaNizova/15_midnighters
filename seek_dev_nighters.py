import requests
import pytz
from datetime import datetime, timezone


def load_attempts():
    pages = 10
    for page in range(1, pages):
        url = 'https://devman.org/api/challenges/solution_attempts/?page={}'
        users = requests.get(url.format(page))
        for user in users.json()['records']:
            yield user


def get_midnighters():
    midnighters = []
    today = datetime.now(timezone.utc)
    for i in load_attempts():
        user_timezone = pytz.timezone(i['timezone'])
        published_date = user_timezone.localize(datetime.fromtimestamp(i['timestamp']))
        # I limited the information about users to one week
        if (today - published_date).days > 7:
            break
        if published_date.hour >= 0 and published_date.hour < 7:
            midnighters.append({'username': i['username'], 'date': published_date})
    return midnighters


if __name__ == '__main__':
    midnighters = get_midnighters()
    uniq_users = set([midnighter['username'] for midnighter in midnighters])
    print('There {} unique users for the last week, who send tasks at night'
          .format(len(uniq_users)))
    for user in uniq_users:
        print(user)
    print('These tasks are:')
    for midnighter in midnighters:
        print('User {} send task on {}'
              .format(midnighter['username'],
                      midnighter['date'].strftime("%H:%M %d.%m.%Y")))
