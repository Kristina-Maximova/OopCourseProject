from abc import ABC, abstractmethod


class VacanciesOperator(ABC):
    """ Класс для работы с вакансиями"""
    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    @abstractmethod
    def add_vacancies(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass

    @abstractmethod
    def del_vacancies(self, *args, **kwargs):
        pass
