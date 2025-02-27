import requests
import json
from src.abstract_api import ApiExplorer


class HH(ApiExplorer):
    """ Класс для работы с API HeadHunter """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'HH-User-Agent': f'OopCourseProject (e-mail)'}
        self.__params = {
            'text': '',
            'search_field': 'name',
            'area': 1,
            'period': 7,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        self.vacancies = []

    # метод должен быть приватным по условию задания.
    # Но при наследовании имя переопределяется, поэтому тут слово с большой буквы
    def _ApiExplorer__may_connect(self) -> bool:  # No error!
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
                    'name': vacancy.get('name'),
                    'salary': vacancy.get('salary', {}).get('from', 0.0),
                    'currency': vacancy.get('salary', {}).get('currency'),
                    'created_at': vacancy.get('created_at'),
                    'url': vacancy.get('url'),
                    'requirement': vacancy.get('snippet', {}).get('requirement'),
                    'schedule': vacancy.get('schedule', {}).get('name')
                }
                result.append(vacancy_data)

            print(f"Найдено вакансий: {len(result)}")
            return result
        print("Не удалось получить данные c hh.ru")
        return []


if __name__ == "__main__":
    hh_obj = HH()
    vac1 = hh_obj.get_vacancies("Python")
    print(vac1)
