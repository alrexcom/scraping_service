import asyncio
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_service.settings")

import django

django.setup()

from work import hhru, superjobru, zarplataru
from scraping.models import *

User = get_user_model()


def get_find_params(language_id, city_id):
    city = City.objects.get(id=city_id)
    language = Language.objects.get(id=language_id)
    return f"| Поисковая строка : {city.name},     {language.name}"


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


# def get_urls(_settings):
#     # qs = Url.objects.all().values()
#     qs = Url.objects.filter(action=True).values()
#     url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
#     urls = []
#     for pair in _settings:
#         tmp = {
#             'city_id': pair[0],
#             'language_id': pair[1],
#             'url_data': url_dict[pair],
#             'params_find': get_find_params(pair[1], pair[0])
#         }
#         urls.append(tmp)
#     return urls


def get_urls(_settings):
    # qs = Url.objects.all().values()
    qs = Url.objects.filter(action=True).values()
    # url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for q in qs:
        tmp = {
            'city_id': q['city_id'],
            'language_id': q['language_id'],
            'url_data': q['url_data'],
            'params_find': get_find_params(q['language_id'], q['city_id'])
        }
        urls.append(tmp)
    return urls


settings_list = get_settings()
urls = get_urls(_settings=settings_list)

parsers = (
    (hhru, 'hhru'),
    (superjobru, 'superjob'),
    (zarplataru, 'zarplataru'),
)

jobs, errors = [], []


# import time
#
# start = time.time()


# Асинхронное выполнение
async def main(value):
    func, url, city_id, language_id, params_find = value
    j, e = await loop.run_in_executor(None, func, url, city_id, language_id, params_find)
    errors.extend(e)
    jobs.extend(j)


# 'params_find': language

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tasks_list = [
    (func, data['url_data'][key], data['city_id'], data['language_id'], data['params_find'])
    for data in urls
    for func, key in parsers
]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tasks_list])
loop.run_until_complete(tasks)
loop.close()

# Последоавтельное выполнение функций 188 с
# for data in urls:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city_id=data['city_id'], language_id=data['language_id'])
#         jobs += j
#         errors += e

# end = time.time()
# print('Time taken: {:.2f}'.format(end - start))

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
        # pass
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
# with open('vacans.txt', 'w', encoding='utf-8') as f:
#     f.write(str(jobs))
