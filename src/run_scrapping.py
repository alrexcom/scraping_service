from work import hhru, superjobru

hh_url = 'https://hh.ru/search/vacancy?text=Python&salary=&ored_clusters=true&area=113&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'

superjob_url = 'https://russia.superjob.ru/vacancy/search/?keywords=Python'

parsers = (
    (hhru, hh_url),
    (superjobru, superjob_url)
)

jobs, errors = [], []

for func, url in parsers:
    j,e = func(url)
    jobs += j
    errors += e

with open('vacans.txt', 'w', encoding='utf-8') as f:
    f.write(str(jobs))


