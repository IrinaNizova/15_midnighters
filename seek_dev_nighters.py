import requests
import pytz
from datetime import datetime, timezone


def get_user_list_from_devman(page):
    url = 'https://devman.org/api/challenges/solution_attempts/'
    return requests.get(url, {'page': page}).json()


def get_user_data(user_records):
    for user in user_records:
        user_timezone = pytz.timezone(user['timezone'])
        pub_date = user_timezone.localize(
            datetime.fromtimestamp(user['timestamp']))
        user['published_date'] = pub_date
        user['is_night'] = True if pub_date.hour >= 0 and pub_date.hour < 7 else False
        yield user


def get_midnighter_commits():
    midnighter_commits = []
    first_page_num = 1
    first_page = get_user_list_from_devman(first_page_num)
    count_pages = first_page["number_of_pages"]
    for page in range(1, count_pages+1):
        user_list = first_page if page==1 else get_user_list_from_devman(page)
        for user in get_user_data(user_list['records']):
            if user['is_night']:
                midnighter_commits.append({'username': user['username'],
                                    'published_date': user['published_date']})
    return midnighter_commits


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
