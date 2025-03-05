import requests

from src.abstract_api import ApiExplorer
from src.mixin_logger import MixinLogger


class HH(ApiExplorer, MixinLogger):
    """ Класс для работы с API HeadHunter """

    def __init__(self):
        """ Конструктор класса для работы с API HeadHunter"""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'HH-User-Agent': 'OopCourseProject (e-mail)'}
        self.__params = {
            'text': '',
            'search_field': 'name',
            'area': 1,
            'period': 7,  # получим данные за последние 7 дней
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        self.vacancies = []
        super().__init__()

    @property
    def url(self):  # геттер
        """ Геттер для параметра url"""
        return self.__url

    @property
    def headers(self):  # геттер
        """ Геттер для параметра headers"""
        return self.__headers

    @property
    def params(self):  # геттер
        """ Геттер для параметра params"""
        return self.__params

    # метод должен быть приватным по условию задания.
    # Но при наследовании имя переопределяется, поэтому тут слово с большой буквы
    def _ApiExplorer__may_connect(self) -> bool:  # No error!
        """ Метод для проверки соединения с сайтом HH.ru"""
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                return True
            else:
                self.log_warning(f"Ошибка запроса {response.status_code}")
                return False
        except ConnectionError:
            self.log_warning("Ошибка соединения с сайтом")
            return False

    def get_vacancies(self, key_word: str) -> list:
        """ Метод для получения вакансий с сайта HH.ru"""
        self.__params['text'] = key_word
        if self._ApiExplorer__may_connect():
            self.log_debug("начат подбор вакансий на hh")
            self.vacancies = []
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                data = response.json()
                self.vacancies += data['items']

                if data['pages'] == self.__params['page']:
                    break
                else:
                    self.__params['page'] += 1
            self.log_debug("ответ получен, приводим данные к словарям для вакансий")
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

            print(f"Всего найдено вакансий: {len(result)}")
            return result
        self.log_warning("Не удалось получить данные c hh.ru")
        return []


if __name__ == "__main__":  # pragma: no cover
    hh_obj = HH()
    vac1 = hh_obj.get_vacancies("Python")
    print(vac1[0])
