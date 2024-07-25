import os, sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_service.settings")

import django

django.setup()

from work import hhru, superjobru
from scraping.models import *

city = City.objects.all().first()
language = Language.objects.all().first()


tema = 'sql'

hh_url = f"https://hh.ru/search/vacancy?text={tema}&salary=&ored_clusters=true&area=113&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"

superjob_url = f"https://russia.superjob.ru/vacancy/search/?keywords={tema}"

parsers = (
    # (hhru, hh_url),
    (superjobru, superjob_url),
)

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e


for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
        # pass
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
# with open('vacans.txt', 'w', encoding='utf-8') as f:
#     f.write(str(jobs))
