import requests
import pickle
import time
import pandas
from bs4 import BeautifulSoup as bs

# Счетчик страниц
def page_counter(max_size):
    for i in max_size:
        try:
            page_number = int(i.text)
        except:
            pass
    return page_number

# Подсчет Страниц SuperJob
def sj_count_page(headers, proxies, request_vacancy):
    sj_url = "https://www.superjob.ru/vacancy/search/"
    last_page = 1
    params = {
        'keywords': {request_vacancy}
    }
    resp = requests.get(sj_url, headers=headers, params=params, proxies=proxies)
    soup = bs(resp.text, 'lxml')
    max_pages = soup.find_all(attrs={"class": "_3hkiy _30F5F _290uh _1tqyb _3PbQP _1AKho"})
    if len(max_pages) != 0:
        last_page = page_counter(max_pages)
    return last_page

# Подсчет Страниц HH
def hh_count_page(headers, proxies, request_vacancy):
    hh_url = "https://hh.ru/search/vacancy"
    last_page = 1
    params = {
        'text': {request_vacancy}
    }
    resp = requests.get(hh_url, headers=headers, params=params, proxies=proxies)
    soup = bs(resp.text, 'lxml')
    max_pages = soup.find_all(attrs={"class": "bloko-button HH-Pager-Control"})
    if len(max_pages) != 0:
        last_page = page_counter(max_pages)
    return last_page

# Получение данных SuperJob
def sj_get(headers, proxies, request_vacancy, last_page):
    sj_url = "https://www.superjob.ru/vacancy/search/"
    i = 1
    while i <= last_page:
        params = {
            'keywords': {request_vacancy},
            'page': {i}
        }
        resp = requests.get(sj_url, headers=headers, params=params, proxies=proxies)
        soup = bs(resp.text, 'lxml')
        sj_vacancies_info = soup.find_all(attrs={"class": "_2g1F-"})

        for vacancy in sj_vacancies_info:
            sj_info = {}
            vacancy_name = vacancy.find(attrs={"class": "_3mfro PlM3e _2JVkc _3LJqf"})
            if vacancy_name is not None:
                name = vacancy_name.text
                sj_info['name'] = vacancy_name.text

            vacancy_salary = vacancy.find(attrs={"class": "_1OuF_ _1qw9T f-test-text-company-item-salary"})
            if vacancy_salary is not None:
                salary = vacancy_salary.text
                salary = salary.replace(u'\xa0', ' ')
                sj_info['salary'] = salary

            vacancy_link = vacancy.find(attrs={"class": "_3mfro PlM3e _2JVkc _3LJqf"})
            try:
                link = vacancy_link.find('a', href=True)
                if link is not None:
                    sj_info['link'] = 'https://www.superjob.ru' + link['href']
                    sj_info['url'] = sj_url
            except:
                pass

            if len(sj_info) != 0:
                vacancies.append(sj_info)
        i += 1
        time.sleep(1)

def hh_get(headers, proxies, request_vacancy, last_page):
    hh_url = "https://hh.ru/search/vacancy"
    i = 1
    while i <= last_page:
        params = {
            'text': {request_vacancy},
            'page': {i}
        }
        resp = requests.get(hh_url, headers=headers, params=params, proxies=proxies)
        soup = bs(resp.text, 'lxml')
        hh_vacancies_info = soup.find_all(attrs={"class": "vacancy-serp-item__row vacancy-serp-item__row_header"})

        for vacancy in hh_vacancies_info:
            hh_info = {}
            vacancy_name = vacancy.find(attrs={"class": "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"})
            if vacancy_name is not None:
                name = vacancy_name.text
                hh_info['name'] = vacancy_name.text

            vacancy_salary = vacancy.find(attrs={"class": "vacancy-serp-item__sidebar"})
            if vacancy_salary is not None:
                salary = vacancy_salary.text
                salary = salary.replace(u'\xa0', ' ')
                hh_info['salary'] = salary

            vacancy_link = vacancy.find('a', attrs={"class": "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"})
            if vacancy_link.has_attr('href'):
                hh_info['link'] = vacancy_link['href']
                hh_info['url'] = hh_url

            if len(hh_info) != 0:
                vacancies.append(hh_info)
        i += 1
        time.sleep(1)

request_vacancy = input("Введите желаемую профессию на русском языке: ")


headers = {
    'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
}

proxies = {
    'http': 'http://3.88.169.225:80',
    # 'https': 'https://165.227.223.19:3128',
}



vacancies = []
sj_count = sj_count_page(headers, proxies, request_vacancy)
sj_vacancy = sj_get(headers, proxies, request_vacancy, sj_count)
hh_count = hh_count_page(headers, proxies, request_vacancy)
hh_vacancy = hh_get(headers, proxies, request_vacancy, hh_count)
df = pandas.DataFrame(columns = ["name", "salary", "link", "url"], data = vacancies)
df.to_csv(r'dataframe.csv', index = True, header = True)
