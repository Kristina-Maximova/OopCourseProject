from abc import ABC, abstractmethod

class ApiExplorer(ABC):
    """ Абстрактный класс для работы со сторонними сервисами через API"""

    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def __may_connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass