import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def get_headers():
    head = Headers(browser='firefox', os='win').generate()
    return head


def multiple_replace(target_str, replace_values):
    for i, j in replace_values.items():
        target_str = target_str.replace(i, j)
    return target_str

hh_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_html, features='html.parser')
vacancy_list = soup.find_all(class_='vacancy-serp-item__layout')

vacancy_list_format = []
for vacancy in vacancy_list:
    vacancy_info = vacancy.find(class_='g-user-content')
    description = vacancy_info.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement',
                                                  'class': 'bloko-text'}).text


    if 'Django' and 'Flask' in description:
    # if 'Python' in description:
        link_vacancy = vacancy.find('a', class_='serp-item__title')['href']
        if vacancy.find('span', class_='bloko-header-section-3') is None:
            salary = 'Уточняйте'
        else:
            salary_tag = vacancy.find('span', class_='bloko-header-section-3').text
            salary = salary_tag.replace('\u202f', ' ')

        company_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        company = company_tag.replace('\xa0', ' ')
        city_tag = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text
        replace_values = {'\xa01\xa0': '', '\xa02\xa0': ''}
        city = multiple_replace(city_tag, replace_values)
        vacancy_list_format.append(
            {
                'link': link_vacancy,
                'salary': salary,
                'company': company,
                'city': city
            })

with open('vacancy.json', 'w') as f:
    json.dump(vacancy_list_format, f, ensure_ascii=False)
pprint(vacancy_list_format)
