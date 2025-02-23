from typing import Any

from src.api_guide import HH


class Vacancy:
    """ Класс для представления вакансии"""

    __slots__ = ("name", "salary", "created_at", "url", "requirement", "schedule")

    def __init__(self, name: str, salary: float | None, created_at: str, url: str, requirement: str, schedule: str):
        """ Конструктор класса вакансия для создания объектов"""
        self.name = name
        self.salary = self.__is_valid_salary(value=salary)
        self.created_at = created_at
        self.url = url
        self.requirement = requirement
        self.schedule = schedule

    def __str__(self) -> str:
        """ Метод строкового отображения вакансии """
        return f"{self.name}, зарплата {self.salary}, url: {self.url}."

    def __eq__(self, other) -> bool:
        """ Метод равенства для сравнения вакансий по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary == compared

    def __ne__(self, other) -> bool:
        """ Метод неравенства для сравнения вакансий по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary != compared

    def __lt__(self, other) -> bool:
        """ Метод меньше для сравнения вакансий по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary < compared

    def __gt__(self, other) -> bool:
        """ Метод больше для сравнения вакансий по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary > compared

    def __le__(self, other) -> bool:
        """ Метод <= для сравнения вакансия по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary <= compared

    def __ge__(self, other) -> bool:
        """ Метод >= для сравнения вакансий по зарплате """
        compared = self._get_compared_operand(other)
        return self.salary >= compared

    @staticmethod
    def _get_compared_operand(other) -> int | float | None:
        """ Получение и валидация сравниваемого значения в операторах сравнения"""
        if not isinstance(other, (int, float, Vacancy)):
            raise TypeError("Сравнение возможно только с объектом класса Vacancy или с числом")
        return other if isinstance(other, (int, float)) else other.salary

    @staticmethod
    def __is_valid_salary(value: Any) -> float:
        """ Метод для валидации данных по зарплате"""
        if value and isinstance(float(value), float):
            return float(value)
        else:
            return 0.0

    @classmethod
    def new_vacancies_obj(cls, data_with_vacancies: list[dict | None]) -> list:
        """ Класс-метод для преобразования списка словарей в список объектов класса"""
        if len(data_with_vacancies) == 0:
            return []
        else:
            new_vacancies_obj = []
            try:
                for vacancy in data_with_vacancies:
                    vacancy_obj = cls(**vacancy)
                    new_vacancies_obj.append(vacancy_obj)
                return new_vacancies_obj
            except AttributeError:
                print("Ошибка преобразования данных в объект класса Vacancy")
                return []


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
    print(vac1)

    print(vac1 > vac2)

    # hh_obj = HH()
    # data_from_hh = hh_obj.get_vacancies('Python')
    # cast_to_list = Vacancy.new_vacancies_obj(data_from_hh)
    # print(cast_to_list[0:3])
