from abc import ABC, abstractmethod
import requests
import json

# это потом в env спрятать надо:
my_gmail = 'tinamaximova21@gmail.com'


class ApiExplorer(ABC):
    """ Абстрактный класс для работы со сторонними сервисами через API"""

    @abstractmethod
    def _may_connect(self):
        pass

    @abstractmethod
    def _get_vacancies(self, *args, **kwargs):
        pass


class HH(ApiExplorer):
    """ Класс для работы с API HeadHunter """

    def __init__(self, database=""):
        self._url = 'https://api.hh.ru/vacancies'
        self._headers = {'HH-User-Agent': f'OopCourseProject ({my_gmail})'}
        self._params = {
            'text': '',
            'search_field': 'name',
            'area': 1,
            'period': 1,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        self.vacancies = []


    def _may_connect(self):
        """ Метод для проверки соединения с сайтом HH.ru"""
        try:
            response = requests.get(self._url, headers=self._headers, params=self._params)
            if response.status_code == 200:
                return True
            else:
                print(f"Ошибка запроса {response.status_code}")
                return False
        except ConnectionError:
            print("Ошибка соединения с сайтом")
            return False


    def _get_vacancies(self, key_word: str) -> list:
        """ Метод для получения вакансий с сайта HH.ru"""
        self._params['text'] = key_word
        if self._may_connect():
            self.vacancies = []
            while True:
                response = requests.get(self._url, headers=self._headers, params=self._params)
                data = response.json()
                self.vacancies += data['items']

                if data['pages'] == self._params['page']:
                    break
                else:
                    self._params['page'] += 1

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
        print("Не удалось получить данные")
        return []


if __name__ == "__main__":
    hh_obj = HH()
    vac1 = hh_obj._get_vacancies("Python developer")
    print(vac1)
