from abc import ABC, abstractmethod

class Vacancies(ABC):
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




class HeadHunterVacncies():
    """ Класс для работы с  вакансиями с сайта HeadHunter"""




if __name__ == "__main__":
    pass
#  проверка на уникальность по ключу 'url'
urls = set()
unique_vacancies = []

for vacancy in vacancies:
    if vacancy['url'] not in urls:
        urls.add(vacancy['url'])
        unique_vacancies.append(vacancy)

print(unique_vacancies)