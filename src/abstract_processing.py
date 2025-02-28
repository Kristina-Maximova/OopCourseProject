from abc import ABC, abstractmethod


class VacanciesProcessing(ABC):
    """ Aбстрактный класс для обработки данных по вакансиям"""

    @abstractmethod
    def __init__(self, vacancies: list, *args, **kwargs):
        """ обязывает в конструкторе иметь аргументом лист с вакансиями"""
        self.vacancies = vacancies  if vacancies else []
        pass

    @abstractmethod
    def sort_vacancies(self, *args, **kwargs):
        """ обязывает определять метод сортировки данных в дочерних классах"""
        pass

    @abstractmethod
    def filter_vacancies(self, *args, **kwargs):
        """ обязывает определять метод фильтрации данных в дочерних классах"""
        pass

