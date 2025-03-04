import datetime
from datetime import timezone

from src.abstract_processing import VacanciesProcessing
from src.mixin_logger import MixinLogger
from src.vacancy import Vacancy


class SalaryAnalyzer(VacanciesProcessing, MixinLogger):
    """ Класс для обработки данных с вакансиями по зарплатe """

    def __init__(self, vacancies: list):
        """
        Конструктор класса для обработки данных по зарплате
        :param vacancies: список объектов класса Vacancy
        """
        super().__init__(vacancies)
        self.vacancies = self.sort_vacancies()

    def sort_vacancies(self):
        """ Метод для сортировки списка объектов класса Vакансии по зарплате"""
        self.log_debug("начата сортировка по зарплате")
        if len(self.vacancies) > 0:
            return sorted(self.vacancies, key=lambda x: x.salary, reverse=True)
        return self.vacancies

    def filter_vacancies(self, lower_limit):
        """ Метод получения списка объектов класса Vacancy
        с зарплатой выше определенного лимита"""
        self.log_debug("начата фильтрация по зарплате")
        if len(self.vacancies) > 0:
            filtered_list = list(vacancy for vacancy in self.vacancies if vacancy >= lower_limit)
            return filtered_list if filtered_list else []


class DateAnalyzer(VacanciesProcessing, MixinLogger):
    """ Класс для обработки данных с вакансиями по дате создания"""

    def __init__(self, vacancies: list):
        """
        Конструктор класса для обработки данных с вакансиями по дате создания
        :param vacancies: список объектов класса Vacancy
        :param date_from: строка с датой в формате ДД.MM.ГГ
        """
        super().__init__(vacancies)
        self.vacancies_no_date = []

    def __enter__(self):
        """ Метод для приведения аргумента вакансий created_at к типу datetime
        и временного удаления вакансий с отсутствующей датой"""
        self.log_debug("начата обработка по дате")
        if len(self.vacancies) > 0:
            # преобразуем дату создания в объект datetime
            self.vacancies = [vacancy.to_datetime() for vacancy in self.vacancies]
            # выбираем вакансии со значением created_at = None и помещаем их в отдельный атрибут
            for vacancy in self.vacancies:
                if not vacancy.created_at:
                    self.vacancies_no_date.append(vacancy)
                    self.vacancies.remove(vacancy)
            return self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> list:
        """ Метод для возвращения типа аргумента вакансий created_at в ISO строку
        и возвращения вакансий без даты в конец списка
        """
        self.log_debug("заканчивается обработка по дате")
        if len(self.vacancies) > 0:
            # возвращаем строковый тип ISO атрибуту created_at
            self.vacancies = [vacancy.to_iso_str() for vacancy in self.vacancies]
            # вакансии с None датой возвращаем в конец списка
            if self.vacancies_no_date:
                for vacancy in self.vacancies_no_date:
                    self.vacancies.append(vacancy)
            return self.vacancies
        return self.vacancies

    def sort_vacancies(self):
        """ Метод для сортировки вакансий по дате создания.
        в начале списка будут последние по дате.
        """
        if len(self.vacancies) > 0:
            with self:
                # сортируем список вакансий с указанной датой
                self.vacancies = sorted(self.vacancies, key=lambda x: x.created_at, reverse=True)
        return self.vacancies

    def filter_vacancies(self, date_from):
        """ Метод для фильтрации вакансий"""
        if len(self.vacancies) > 0:
            try:
                # Создаем offset-naive datetime
                formated_date = datetime.datetime.strptime(date_from, "%d.%m.%y")
                # Преобразуем его в offset-aware datetime, т.к. такой тип в вакансиях
                formated_date = formated_date.replace(tzinfo=timezone.utc)
                with self:
                    filtered_list = list(vacancy for vacancy in self.vacancies if vacancy.created_at >= formated_date)
                    return filtered_list
            except Exception as e:
                self.log_warning(f"Фильтрация по дате  не проведена, ошибка: {e}")
                return self.vacancies


if __name__ == "__main__":  # pragma: no cover
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

    # печать линии в консоли:
    print('-' * 200)

    analyzer1 = SalaryAnalyzer(my_list)
    my_list1 = analyzer1.filter_vacancies(2100)
    for vac in my_list1:
        print(vac)
    print('-' * 200)
    # analyser2 = DateAnalyzer(my_list)
    # my_list2 = analyser2.sort_vacancies()
    # for vac in my_list2:
    #     print(vac, vac.created_at, type(vac.created_at))

    # filtered_by_date_list = analyser2.filter_vacancies("21.02.25")
    #
    # for vac in filtered_by_date_list:
    #     print(vac, vac.created_at)
    # print('-' * 200)
