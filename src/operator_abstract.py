from abc import ABC, abstractmethod


class VacanciesOperator(ABC):
    """ Класс для работы с вакансиями"""

    @abstractmethod
    def add_vacancies(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass

    @abstractmethod
    def del_vacancies(self, *args, **kwargs):
        pass
