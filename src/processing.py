from src.abstract_processing import VacanciesProcessing
from src.vacancy import Vacancy
import datetime


class SalaryAnalyzer(VacanciesProcessing):
    """ Класс для обработки данных с вакансиями по зарплатe """

    def __init__(self, vacancies: list, lower_limit: float=0.0):
        """
        Конструктор класса для обработки данных по зарплате
        :param vacancies: список объектов класса Vacancy
        :param salary_lower_limit:
        """
        super().__init__(vacancies)
        self.vacancies = self.sort_by_salary()
        self.lower_limit = lower_limit


    def sort_by_salary(self):
        """ Метод для сортировки списка объектов класса Vакансии по зарплате"""
        if len(self.vacancies) > 0:
            return sorted(self.vacancies, key=lambda x: x.salary, reverse=True)
        return self.vacancies


    def filter_by_salary(self, lower_limit):
        """ Метод для фильтрации списка объектов класса Vакансии выше определенного лимита"""
        if len(self.vacancies) > 0:
            filtered_list = list(vacancy for vacancy in self.vacancies if vacancy >= lower_limit)
            return filtered_list if filtered_list else []



class DateAnalyzer(VacanciesProcessing):

    def __init__(self, vacancies: list):
        super().__init__(vacancies)

    def sort_by_date(self):

        for vacancy in self.vacancies:
            vacancy.created_at = datetime.datetime.fromisoformat(vacancy.created_at)

        self.vacancies = sorted(self.vacancies, key=lambda x: x.created_at)

        for vacancy in self.vacancies:
            vacancy.created_at.isoformat()
        return self.vacancies

    def filter_by_date(self):
        pass




if __name__ == "__main__":
    vac1 = Vacancy(**{'name': 'Middle Backend Developer (Python FastAPI + SQL)',
                      'salary': 21,
                      'currency': "RUR",
                      'created_at': '2025-02-21T14:46:49+0300',
                      'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
                      'requirement': 'Написание качественного кода и тестов к нему. '
                                     'Необходимый стек: <highlighttext>Python</highlighttext> (asyncio), '
                                     'чистый SQL (не ORM), FastAPI (весь функционал), микросервисная архитектура...',
                      'schedule': 'Удаленная работа',
                      })
    vac2 = Vacancy(**{'name': 'Python-разработчик',
                      'salary': 80000,
                      'currency': "RUR",
                      'created_at': '2025-02-11T14:00:01+0300',
                      'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                      'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>. '
                                     'Умение структурно мыслить, а также разбивать проект на подзадачи. '
                                     'Опыт с другими языками программирования, например...',
                      'schedule': 'Полный день',
                      })
    vac3 = Vacancy(**{'name': "test3",
                      'salary': 0.03,
                      'currency': "RUR",
                      'created_at': '2025-02-20T14:46:49+0300',
                      'url': "test_url3",
                      'requirement': "test_requirement3",
                      'schedule': "test_schedule3",
                      })
    vac4 = Vacancy(**{'name': "test4",
                      'salary': 4.04,
                      'currency': "RUR",
                      'created_at': '2025-02-25T14:46:49+0300',
                      'url': "test_url4",
                      'requirement': "test_requirement4",
                      'schedule': "test_schedule4",
                      })
    my_list = [vac1, vac2, vac3, vac4]


    analyzer1 = SalaryAnalyzer(my_list)
    my_list1 = analyzer1.vacancies
    for vac in my_list1:
        print(vac)

    analyser2 = DateAnalyzer(my_list1)
    my_list2 = analyser2.sort_by_date()
    for vac in my_list2:
        print(vac, vac.created_at)



