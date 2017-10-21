import requests
import pytz
from datetime import datetime, timezone


def get_user_list_from_devman(page):
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


def get_midnighter_commits():
    midnighters = []
    first_page_num = 1
    first_page = get_user_list_from_devman(first_page_num)
    count_pages = first_page["number_of_pages"]
    for page in range(1, count_pages+1):
        user_list = first_page if page==1 else get_user_list_from_devman(page)
        for user in get_user_data(user_list):
            if user['is_night']:
                midnighters.append({'username': user['username'],
                                    'published_date': user['published_date']})
    return midnighters


if __name__ == '__main__':
    midnighter_commits = get_midnighter_commits()
    uniq_users = set([commit['username'] for commit in midnighter_commits])
    print('There {} unique users, who create commits at night'
          .format(len(uniq_users)))
    for uniq_user in uniq_users:
        print(uniq_user)

    print('List of commits:')
    for midnighter_commit in midnighter_commits:
        print('User {} send task on {}'
              .format(midnighter_commit['username'],
                      midnighter_commit['published_date']
                      .strftime("%H:%M %d.%m.%Y")))
