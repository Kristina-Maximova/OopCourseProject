import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import os


class VacanciesOperator(ABC):
    """ Класс для работы с вакансиями"""

    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancy(self, *args, **kwargs):
        pass

    @abstractmethod
    def del_vacancy(self, *args, **kwargs):
        pass


class JsonOperator(VacanciesOperator):
    """ Класс для сохранения информации о вакансиях в JSON-файл """

    def __init__(self, source_name: str, source_url: str, vacancies_list: list, file_path: str = ""):
        """ Конструктор класса для обработки данных с вакансиями и записи их в json-файл """
        self.source_name = source_name
        self.source_url = source_url
        self.__file_path = file_path if file_path else f"..\\data\\{source_name.replace(' ', '_')}_vacancies.json"
        self.vacancies_list = vacancies_list

    def load_vacancies(self):
        """ Метод для загрузки вакансий из json-файла.
        Вакансии добавляются в список с вакансиями в этом объекте """
        try:
            with open(self.__file_path, 'r+', encoding='utf-8') as file1:
                data = json.load(file1)
        except FileNotFoundError:
            print(f"Файл {self.__file_path} не найден")
        except json.decoder.JSONDecodeError:  # например, если файл пустой, будет такая ошибка
            print(f"Ошибка получения данных из файла {self.__file_path}")
        else:
            if data:
                for vacancy in data:
                    if Vacancy(**vacancy) not in self.vacancies_list:
                        self.vacancies_list.append(Vacancy(**vacancy))

    def write_vacancies(self):
        """ Метод для записи вакансий в файл"""
        self.load_vacancies()
        data = []  # json-файл не должен быть совсем пустым, задаем пустой список
        if len(self.vacancies_list) > 0:
            for vacancy in self.vacancies_list:
                data.append(vacancy.to_dict)
        try:
            with open(self.__file_path, "w+", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print(f"Файл {self.__file_path} не найден")
        except json.decoder.JSONDecodeError:
            print("Ошибка, данные не записаны в файл")

    def add_vacancy(self, vacancy):
        """ Метод добавления одного объекта класса Vacancy в json-файл"""
        if isinstance(vacancy, Vacancy):
            self.load_vacancies()
            if vacancy not in self.vacancies_list:
                self.vacancies_list.append(vacancy)
            self.write_vacancies()
        else:
            raise TypeError("Внести в базу можно только объект класса Vacancy")

    def get_vacancy(self, criteria: dict):
        """ Метод для получения из json-файла вакансии с заданными критериями """
        pass

    def del_vacancy(self, criteria: dict):
        pass


if __name__ == "__main__":
    vac1 = Vacancy(**{'name': 'Middle Backend Developer (Python FastAPI + SQL)',
                      'salary': 210000,
                      'created_at': '2025-02-21T14:46:49+0300',
                      'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
                      'requirement': 'Написание качественного кода и тестов к нему. '
                                     'Необходимый стек: <highlighttext>Python</highlighttext> (asyncio), '
                                     'чистый SQL (не ORM), FastAPI (весь функционал), микросервисная архитектура...',
                      'schedule': 'Удаленная работа'})
    vac2 = Vacancy(**{'name': 'Python-разработчик',
                      'salary': 80000,
                      'created_at': '2025-02-21T14:00:01+0300',
                      'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                      'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>. '
                                     'Умение структурно мыслить, а также разбивать проект на подзадачи. '
                                     'Опыт с другими языками программирования, например...',
                      'schedule': 'Полный день'})
    vac3 = Vacancy(**{'name': "test3",
                      'salary': 0.03,
                      'created_at': "test_date3",
                      'url': "test_url3",
                      'requirement': "test_requirement3",
                      'schedule': "test_schedule3"})
    vac_to_json1 = JsonOperator("HeadHunter", "https://hh.ru", [vac1, vac2])

    vac_to_json1.write_vacancies()
    print(f"вакансий в списке объекта: {len(vac_to_json1.vacancies_list)}")
