from abc import ABC, abstractmethod
import requests
import json


class ApiExplorer(ABC):
    """ Абстрактный класс для работы со сторонними сервисами через API"""

    @abstractmethod
    def __may_connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class HH(ApiExplorer):
    """ Класс для работы с API HeadHunter """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'HH-User-Agent': f'OopCourseProject (e-mail)'}
        self.__params = {
            'text': '',
            'search_field': 'name',
            'area': 1,
            'period': 1,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        self.vacancies = []


    def _ApiExplorer__may_connect(self) -> bool:
        """ Метод для проверки соединения с сайтом HH.ru"""
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                return True
            else:
                print(f"Ошибка запроса {response.status_code}")
                return False
        except ConnectionError:
            print("Ошибка соединения с сайтом")
            return False

    def get_vacancies(self, key_word: str) -> list:
        """ Метод для получения вакансий с сайта HH.ru"""
        self.__params['text'] = key_word
        if self._ApiExplorer__may_connect():
            self.vacancies = []
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                data = response.json()
                self.vacancies += data['items']

                if data['pages'] == self.__params['page']:
                    break
                else:
                    self.__params['page'] += 1

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
    vac1 = hh_obj.get_vacancies("Python")
    print(vac1)
