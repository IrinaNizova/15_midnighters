import requests
import pytz
from datetime import datetime, timezone

def load_attempts():
    pages = 10
    for page in range(1, pages):
        r = requests.get('https://devman.org/api/challenges/solution_attempts/?page={}'.format(page))
        for user in r.json()['records']:
            yield user

def get_midnighters():
    midnighters = []
    today = datetime.now(timezone.utc)
    for i in load_attempts():
        user_timezone = pytz.timezone(i['timezone'])
        published_date = user_timezone.localize(datetime.fromtimestamp(i['timestamp']))
        if (today - published_date).days > 3:
            break
        if published_date.hour >=0 and published_date.hour <=7:
            midnighters.append((i['username'], published_date))
    return midnighters

if __name__ == '__main__':
    print(get_midnighters())
