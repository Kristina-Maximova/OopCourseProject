from abc import ABC, abstractmethod


class VacanciesProcessing(ABC):
    """ Aбстрактный класс для обработки данных по вакансиям"""

    @abstractmethod
    def __init__(self, vacancies: list, *args, **kwargs):
        """ обязывает в конструкторе иметь аргументом лист с вакансиями"""
        self.vacancies = vacancies  if vacancies else []
        pass

    # @abstractmethod
    # def process(self, *args, **kwargs):
    #     """ обязывает определять метод обработки данных в дочерних классах"""
    #     pass


