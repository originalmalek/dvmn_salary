import requests
from dotenv import load_dotenv
import os
from itertools import count
from terminaltables import AsciiTable


def get_top_languages(languages, area):
    top_languages = []

    url = 'https://api.hh.ru/vacancies'
    for language in languages:
        payload = {'text': f'Программист !{language}',
                   'area': area,
                   'per_page': 100}

        response = requests.get(url, params=payload)
        response.raise_for_status()
        response_hh = response.json()
        if response_hh['found'] > 100:
            top_languages.append(language)
    return top_languages


def predict_salary(payment_from, payment_to):
    if payment_from != 0 and payment_to != 0:
        return (payment_from + payment_to) / 2
    if payment_from != 0 and payment_to == 0:
        return payment_from * 1.2
    if payment_from == 0 and payment_to != 0:
        return payment_to * 0.8
    return None


def count_vacancies_hh(top_languages, area):
    url = 'https://api.hh.ru/vacancies'
    data_languages_hh = {}

    for language in top_languages:
        vacancies_processed = 0
        salary_amount = 0
        average_salary = 0

        payload = {'text': f'Программист !{language}',
                   'area': area,
                   'per_page': 100}

        for page in count(0):
            payload.update({'page': page})

            response = requests.get(url, params=payload)
            response.raise_for_status()
            response_hh = response.json()

            for item in response_hh['items']:
                if item['salary'] is not None and item['salary']['currency'] == 'RUR':
                    payment_from = 0 if item['salary']['from'] == None else item['salary']['from']
                    payment_to = 0 if item['salary']['to'] == None else item['salary']['to']
                else:
                    payment_from = 0
                    payment_to = 0

                salary = predict_salary(payment_from, payment_to)

                if salary:
                    salary_amount += salary
                    vacancies_processed += 1

            if response_hh['pages'] == page + 1:
                break
        try:
            average_salary = int(salary_amount / vacancies_processed)
        except ZeroDivisionError:
            average_salary = 0
            vacancies_processed = 0
        data_languages_hh.update({language:
                                      {'vacancies_found': response_hh['found'],
                                       'average_salary': average_salary,
                                       'vacancies_processed': vacancies_processed}})
    return sorted(data_languages_hh.items(), key=lambda x: x[1]['average_salary'], reverse=True)


def count_vacancies_sj(top_languages, superjob_token, area_sj):
    url = 'https://api.superjob.ru/2.33/vacancies/'
    header = {'X-Api-App-Id': superjob_token}

    data_languages_sj = {}

    for language in top_languages:
        vacancies_processed = 0
        salary_amount = 0
        average_salary = 0
        count_per_page = 100

        payload = {'keyword': f'Программист !{language}',
                   'town': area_sj,
                   'count': count_per_page}

        for page in count(0):
            payload.update({'page': page})

            response = requests.get(url, headers=header, params=payload)
            response.raise_for_status()
            response_superjob = response.json()

            for object_sj in response_superjob['objects']:
                salary = predict_salary(object_sj['payment_from'], object_sj['payment_to'])
                if salary:
                    salary_amount += salary
                    vacancies_processed += 1

            if response_superjob['total'] // count_per_page == page:
                break

        try:
            average_salary = int(salary_amount / vacancies_processed)
        except ZeroDivisionError:
            average_salary = 0
            vacancies_processed = 0
        data_languages_sj.update({language:
                                 {'vacancies_found': response_superjob['total'],
                                  'average_salary': average_salary,
                                  'vacancies_processed': vacancies_processed}})

    return sorted(data_languages_sj.items(), key=lambda x: x[1]['average_salary'], reverse=True)


def print_table(table_title, data_languages_hh):
    title = table_title
    print_data = [['Programming Language', 'Vacancies Found', 'Vacancies Processed', 'Average Salary']]

    for language in data_languages_hh:
        print_data.append([language[0],
                           language[1]['vacancies_found'],
                           language[1]['vacancies_processed'],
                           language[1]['average_salary']])

    table_instance = AsciiTable(print_data, title)
    for i in range(4):
        table_instance.justify_columns[i] = 'center'
    print(table_instance.table)


def main():
    load_dotenv()
    superjob_token = os.getenv('SUPERJOB_TOKEN')

    languages = ['Java', 'Python', 'C++', 'C#', 'Vusual Basic',
                 'Javascript', 'R', 'PHP', 'Swift', 'Go', 'Perl', 'Scala']

    area_hh = 1  # Moscow
    area_sj = 4  # Moscow

    top_languages = get_top_languages(languages, area_hh)

    data_languages_hh = count_vacancies_hh(top_languages, area_hh)
    data_languages_sj = count_vacancies_sj(top_languages, superjob_token, area_sj)

    print_table('HH Average Salary', data_languages_hh)
    print_table('SJ Average Salary', data_languages_sj)


if __name__ == '__main__':
    main()
