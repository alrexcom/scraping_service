from datetime import datetime
import json
import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

# from django.core.serializers import json

# Подсовываем кто я  для сервера
headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
]




notneed = ['преподаватель', 'учитель', 'педагог','школу', 'школа','тьютор']


def not_needed_records(title):
    return any(keyword in title.lower() for keyword in notneed)


def hhru(url_):
    # print(response.text)
    # url_ = ('https://hh.ru/search/vacancy?text=Python&salary=&ored_clusters=true&area=113&hhtmFrom=vacancy_search_list'
    #         '&hhtmFromLabel=vacancy_search_line')
    errors = []
    jobs = []
    data = []
    headers_ = headers[randint(0, len(headers) - 1)]
    response = requests.get(url_, headers=headers_)
    if response.status_code == 200:
        soup = BS(response.text, 'html.parser')
        # main_div=soup.find_all('div', class_='vacancy_list')
        main_div = soup.find('div', id='a11y-main-content')
        div_list = main_div.find_all('div', class_='vacancy-search-item__card')

        for div in div_list:
            title_card = div.find('h2', class_='bloko-header-section-2')
            if title_card:
                opyt = div.find('span', {'data-qa': 'vacancy-serp__vacancy-work-experience'})
                if opyt:
                    opyt = opyt.text

                title = title_card.text
                if not not_needed_records(title):
                    title_url = title_card.a['href']
                    # На другой странице по ссылке на вакансию подробнее
                    data = get_details(title_url, headers_)
                    domain = "https://hh.ru"
                    company_url = div.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
                    company = company_url.span.text

                    # city = div.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).span.text

                    # print(f"{title} || {opyt} ||{city}|| Фирма '{firma}' https://hh.ru/{firma_url['href']}")
                    company_url = domain + company_url['href']

                    jobs.append(
                        {
                         'site': domain,
                         'title': title,
                         'url': title_url,
                         'opyt': opyt,
                         # 'city': city,
                         'company': company,
                         'company_url': company_url,
                         } | data
                    )
                # print(jobs)
            else:
                errors.append({'url': url_, 'error': 'title_card не найден'})
            # print(title)
    else:
        errors.append({'url': url_, 'error': response.status_code})

    return jobs, errors + data['errors_url']


def get_details(urls_, headers_):
    # url_='https://armavir.hh.ru/vacancy/103984269?query=Delphi&hhtmFrom=vacancy_search_list'
    response_ = requests.get(urls_, headers=headers_)
    # with codecs.open('job.html', 'w', 'UTF-8') as f:
    #     f.write(str(response.text))

    description = 'нет описания'
    salary = 'не указана зарплата'
    job_day = 'длительность рабочего дня не указана'
    date_public = 'дата публикации не указана'
    address = 'нет адреса'
    logo_url = ''
    skills = []
    errors = []
    if response_.status_code == 200:
        soup = BS(response_.text, 'html.parser')

        description = soup.find('div', {'data-qa': "vacancy-description"})
        if description:
            # description = description

            job_day = soup.find('p', {'data-qa': "vacancy-view-employment-mode"})
            if job_day:
                job_day = job_day.text

            salary = soup.find('div', class_='vacancy-title')
            if salary:
                salary = salary.span.text

            if soup.find('div', class_='vacancy-company-logo-redesigned'):
                logo_url = soup.find('div', class_='vacancy-company-logo-redesigned').img.get('src')

            skills = [t.string for t in soup.findAll('li', {'data-qa': 'skills-element'})]

            date_public = soup.find('p', class_='vacancy-creation-time-redesigned')
            if date_public:
                date_public = date_public.text
                date_public = date_public.split(" ")[2]
            # date_public = datetime.strptime(date_string, "%d\xa0%B\xa0%Y")

            # date_public=datetime.strptime(date_public.split(" ")[2], "%d %B %Y")

            address = soup.find('div', {'data-qa': 'vacancy-company'})
            # if address:
            #     address = address.text
        else:
            errors.append({'url': urls_, 'error': 'нет тэга vacancy-description'})

    else:
        errors.append({'url': urls_, 'error': response_.status_code})

    return {'description': str(description),
            'salary': str(salary),
            'job_day': str(job_day),
            'logo_url': logo_url,
            'date_public': str(date_public),
            'address': str(address),
            'skills': str(skills),
            'errors_url': errors}


def superjobru(url_):
    # print(response.text)
    domain = "https://russia.superjob.ru"
    # url_ = ('https://russia.superjob.ru/vacancy/search/?keywords=Python')
    errors = []
    jobs = []
    data = []
    headers_ = headers[randint(0, len(headers) - 1)]
    response = requests.get(url_, headers=headers_)

    if response.status_code == 200:
        soup = BS(response.text, 'html.parser')
        # main_div=soup.find_all('div', class_='vacancy_list')
        main_div = soup.find('div', class_="-lWKU _3pduz")
        div_list = main_div.find_all('div', class_='f-test-search-result-item')

        for div in div_list:
            # print(div.prettify())
            title_card = div.a
            if title_card:
                title = title_card.text
                if not not_needed_records(title):

                    title_url = domain + title_card['href']
                    salary = div.find("div", class_="f-test-text-company-item-salary")
                    if salary:
                        salary = salary.text
                    logo = div.find('img')
                    if logo:
                        logo_url = div.find('img').get('src')

                    company = div.find('span', class_='f-test-text-vacancy-item-company-name')
                    if company:
                        company_url = domain + company.a['href']
                        company = company.get_text(strip=True)

                    city = div.find('span', class_='_3a7uW _2myqe _3r0vg _3agHj')
                    if city:
                        city = city.get_text(strip=True)

                    date_public = div.find('span', class_='_3a7uW _2myqe _3FVnJ _3agHj')
                    if date_public:
                        date_public = date_public.get_text(strip=True)

                    address = div.find('span', class_='f-test-text-company-item-location')
                    if not address:
                        address = div.find('span', class_='_3a7uW _2myqe _3r0vg _3agHj')

                    if not address:
                        address = div.find('span', class_='_3-Il9 _11FhW ayzah dYQFr _3a7uW _2myqe _3r0vg _3agHj')

                    if address:
                        address = f"<div> {address.get_text(strip=True)} </div>"
                    else:
                        address = "не удалось определить адрес"

                    data = details_superjob(title_url, headers_)

                    jobs.append({
                                    'site': domain,
                                    'title': title,
                                    'url': title_url,
                                    # 'city': city,
                                    'company': company, 'company_url': company_url,
                                    'address': address, "logo_url": logo_url, "salary": salary,
                                    'date_public': date_public} | data)
                # print(jobs)
            else:
                errors.append({'url': url_, 'error': 'title_card не найден'})
            # print(title)
    else:
        errors.append({'url': url_, 'error': response.status_code})

    return jobs, errors + data['errors_url']


def details_superjob(urls_, headers_):
    errors = []
    response_ = requests.get(urls_, headers=headers_)
    if response_.status_code == 200:
        soup = BS(response_.text, 'html.parser')
        main_div = soup.find('div', class_="f-test-vacancy-base-info")
        if main_div:
            opyt = main_div.find('div', class_="-lWKU _2O5D_ _11FhW ayzah _1LL-n")
            if opyt:
                opyt = opyt.get_text(strip=True)

            description = main_div.find('span', class_="mrLsm _3a7uW _2myqe _3r0vg _3agHj _1zcvm")
            if description:
                description = f"<div> {description} </div>"
            #     description = description.get_text(strip=True)

            skills = main_div.find('div', class_="-lWKU _3XDe- _1zFiz _3Oc5C _3p5Fx")
            if skills:
                skills = [t.get_text(strip=True) for t in skills.findAll('li')]

        else:
            errors.append({'url': urls_, 'error': 'не нйден div f-test-vacancy-base-info'})

    else:
        errors.append({'url': urls_, 'error': 'нет доступа к ссылке подробнее'})

    return {'description': description, 'opyt': opyt, 'skills': str(skills),
            'errors_url': errors}

# if __name__ == '__main__':
#     jobs_superjob, errors_superjob = superjobru()
#
#     jobs_hh, errors_hh = hhru()
#
#     with open('vacans.txt', 'w', encoding='utf-8') as f:
#         f.write(str(jobs_hh + jobs_superjob))
#
#     print("ok")
