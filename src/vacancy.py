from typing import Any

from src.api_exchange_rate import get_usd_rate
from src.api_guide import HH
from src.mixin_logger import MixinLogger
import datetime


class Vacancy(MixinLogger):
    """ Класс для представления вакансии"""
    vacancies_counter = 0
    __slots__ = ("name", "salary", "currency", "created_at", "url", "requirement", "schedule", "vac_id",)
    # так как в слотах нецелесообразно прописывать ("logger", "filehandler", "file_formatter"),
    # logger работает только в инициализаторе


    def __init__(self, name: str, salary: float | None, currency: str, created_at: str | datetime.datetime ,
                 url: str, requirement: str, schedule: str, vac_id: int = None):
        """ Конструктор класса вакансия для создания объектов"""
        self.name = name
        self.currency = currency
        self.salary = self.__is_valid_salary(value=salary)
        self.created_at = created_at
        self.url = url
        self.requirement = requirement
        self.schedule = schedule
        self.currency = "RUR"  # в идеале менять в методе is_valid_salary при конвертации, пока так не получилось
        if not vac_id:
            Vacancy.vacancies_counter += 1
        self.vac_id = vac_id if vac_id else Vacancy.vacancies_counter
        super().__init__()
        self.log_debug(f"Создана вакансия {self.vac_id}")

    def __str__(self) -> str:
        """ Метод строкового отображения вакансии """
        return f"{self.vac_id}: {self.name}, зарплата {self.salary}, url: {self.url}."

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

    @property
    def to_dict(self):  # с декоратором вызов без круглых скобок
        return {"name": self.name,
                "salary": self.salary,
                "currency": self.currency,
                "created_at": self.created_at,
                "url": self.url,
                "requirement": self.requirement,
                "schedule": self.schedule,
                "vac_id": self.vac_id}

    @staticmethod
    def _get_compared_operand(other) -> int | float | None:
        """ Получение и валидация сравниваемого значения в операторах сравнения"""
        if not isinstance(other, (int, float, Vacancy)):
            raise TypeError("Сравнение возможно только с объектом класса Vacancy или с числом")
        return other if isinstance(other, (int, float)) else other.salary

    # ? как переводить зп в USD в руб, не увеличивая количество слотов

    def __is_valid_salary(self, value: Any) -> float:
        """ Метод для валидации данных по зарплате
        Если во входящих данных указана в USD, по-умолчанию переводится в руб. """
        if value and isinstance(float(value), float):
            if self.currency == "USD":
                curs = get_usd_rate()
                new_value = round(float(value) * curs, 2)
                return new_value
            return value
        else:
            return 0.0

    @classmethod
    def cast_to_object_list(cls, data_with_vacancies: list[dict | None]) -> list:
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
                      'currency': 'RUR',
                      'created_at': '2025-02-21T14:46:49+0300',
                      'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
                      'requirement': 'Написание качественного кода и тестов к нему. '
                                     'Необходимый стек: <highlighttext>Python</highlighttext> (asyncio), '
                                     'чистый SQL (не ORM), FastAPI (весь функционал), микросервисная архитектура...',
                      'schedule': 'Удаленная работа',

                      })
    vac2 = Vacancy(**{'name': 'Python-разработчик',
                      'salary': 1500,
                      'currency': 'USD',
                      'created_at': '2025-02-21T14:00:01+0300',
                      'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                      'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>. '
                                     'Умение структурно мыслить, а также разбивать проект на подзадачи. '
                                     'Опыт с другими языками программирования, например...',
                      'schedule': 'Полный день',

                      })
    print(vac1)
    print(type(vac1))
    print(vac1.salary, vac1.currency)
    print(vac2.salary, vac2.currency)

    print(vac1 > vac2)

    # hh_obj = HH()
    # data_from_hh = hh_obj.get_vacancies('Python')
    # casted_to_list_vacs = Vacancy.cast_to_object_list(data_from_hh)
    # for elem in casted_to_list_vacs[0:3]:
    #     print(elem)
