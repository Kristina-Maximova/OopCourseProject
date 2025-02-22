from abc import ABC, abstractmethod
import requests
import json

# это потом в env спрятать надо:
my_gmail = 'tinamaximova21@gmail.com'


class ApiExplorer(ABC):
    """ Абстрактный класс для работы со сторонними сервисами через API"""

    def get_vacancies(self, *args, **kwargs):
        pass


class HH(ApiExplorer):
    """ Класс для работы с API HeadHunter """

    def __init__(self, database=""):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'HH-User-Agent': f'OopCourseProject ({my_gmail})'}
        self.params = {
            'text': '',
            'search_field': 'name',
            'area': 1,
            'period': 1,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        self.vacancies = []


    def get_vacancies(self, key_word):

        self.params['text'] = key_word

        self.vacancies = []
        while True:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            data = response.json()
            self.vacancies += data['items']

            if data['pages'] == self.params['page']:
                break
            else:
                self.params['page'] += 1

        result = []
        for vacancy in self.vacancies:
            vacancy_data = {
                'name': vacancy['name'],
                'salary': vacancy['salary']['from'] if vacancy['salary']['from'] is not None else 0.0,
                'created_at': vacancy['created_at'],
                'url': vacancy['url'],
                'requirement': vacancy['snippet']['requirement'],
                'schedule': vacancy['schedule']['name']

            }
            result.append(vacancy_data)

        print(f"Найдено вакансий: {len(result)}")
        return result


if __name__ == "__main__":
    hh_obj = HH()
    vac1 = hh_obj.get_vacancies("Python developer")
    print(vac1)