import json
import os
from src.mixin_logger import MixinLogger
from src.abstract_operator import VacanciesOperator
from src.vacancy import Vacancy


class JsonOperator(VacanciesOperator, MixinLogger):
    """ Класс для сохранения информации о вакансиях в JSON-файл """

    def __init__(self, source_name: str, source_url: str, vacancies_list: list, file_path: str = ""):
        """ Конструктор класса для обработки данных с вакансиями и записи их в json-файл """
        self.source_name = source_name
        self.source_url = source_url
        self.__file_path = file_path if file_path else self._get_file_name(source_name)
        self.vacancies_list = vacancies_list if vacancies_list else []
        super().__init__()

    # Методы __enter__ и __exit__ позволяют создать контекстный менеджер для работы с json-файлом
    def __enter__(self):
        """ Метод для получения данных о вакансиях из json-файла"""
        try:
            with open(self.__file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.log_info(f"Файл {self.__file_path} не найден и будет создан заново")
        except json.decoder.JSONDecodeError:  # например, если файл пустой, будет такая ошибка
            print(f"Ошибка получения данных из файла {self.__file_path}")
        else:
            if data:
                try:
                    for vacancy in data:
                        if Vacancy(**vacancy) not in set(self.vacancies_list):
                            self.vacancies_list.append(Vacancy(**vacancy))
                    # return self.vacancies_list
                except TypeError as e:
                    self.log_warning(f"Данные в файле не читаются как вакансии: {e}")
        finally:
            self.log_info(f"в базе вакансий было: {len(self.vacancies_list)}")
            return self.vacancies_list

    # ? Задача на доделать: как переписывать только определенную страницу в большом файле.
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Метод для передачи данных из объекта в json-файл """
        data = []  # json-файл не должен быть совсем пустым
        if len(self.vacancies_list) > 0:
            for vacancy in self.vacancies_list:
                data.append(vacancy.to_dict)
            try:
                with open(self.__file_path, "w+", encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except json.decoder.JSONDecodeError:
                self.log_warning("Ошибка, данные не записаны в файл")
            except FileNotFoundError:
                self.log_warning("Файл не найден")
            else:
                self.log_info(f"в базе вакансий стало: {len(self.vacancies_list)}")
        else:
            self.log_info("Нет данных для записи")

    @property
    def file_path(self):
        """ Геттер для получения атрибута
         К атрибуту можно обращаться без ()"""
        return self.__file_path

    @file_path.setter
    def file_path(self, new_path: str):
        """ Сеттер. Метод срабатывает при операции присваивания
        нового значения у уже созданного объекта """
        self.__file_path = new_path

    def add_vacancy(self, new_vacancy):
        """ Добавляет объект класса Vacancy  в json-файл"""
        with self:
            if isinstance(new_vacancy, Vacancy) and not new_vacancy in set(self.vacancies_list):
                self.vacancies_list.append(new_vacancy)

    def get_vacancy(self, vac_id: int) -> None | Vacancy:
        """ Получает объект класса Vacancy из json-файла по номеру id"""
        with self:
            for vacancy in self.vacancies_list:
                if vacancy.vac_id == vac_id:
                    return vacancy

    def del_vacancy(self, unwanted_vacancy):
        """ Удаляет объект класса Vacancy из json-файла"""
        with self:
            if unwanted_vacancy in set(self.vacancies_list):
                self.vacancies_list.remove(unwanted_vacancy)

    def add_vacancies(self, vacancies: list):
        """ Метод добавления списка объектов класса Vacancy в json-файл"""
        if vacancies:
            with self:
                for vacancy in vacancies:
                    if not isinstance(vacancy, Vacancy):
                        raise TypeError("Внести в базу можно только объект класса Vacancy")
                    elif vacancy not in set(self.vacancies_list):
                        self.vacancies_list.append(vacancy)
                self.log_debug(f"работает add_vacancies, в списке {len(self.vacancies_list)}")
                return self

    def get_vacancies(self, criteria: dict) -> list | None:
        """ Метод для получения из json-файла вакансий с заданными критериями
         criteria: параметр и его значение у вакансий, которые надо получить.
         Возвращает список вакансий, соответствующий критериям
         """
        if self.is_valid_criteria(criteria):
            with self:
                filtered_vacancies = []
                if len(self.vacancies_list) > 0:
                    for key, value in criteria.items():
                        filtered_vacancies = [vacancy for vacancy in self.vacancies_list if
                                              getattr(vacancy, key) == value]
                self.log_info(f"найдено вакансий по критериям: {len(filtered_vacancies)}")
                return filtered_vacancies
        return []

    def del_vacancies(self, criteria: dict):
        """ Метод для удаления нескольких вакансий из json-файла """
        if self.is_valid_criteria(criteria):
            with self:
                list_to_delete = []
                if len(self.vacancies_list) > 0:
                    for key, value in criteria.items():
                        list_to_delete = [vacancy for vacancy in self.vacancies_list if
                                          getattr(vacancy, key) == value]
                    if list_to_delete and len(list_to_delete) > 0:
                        print(f"Будет удалено вакансий: {len(list_to_delete)}")
                        new_list = [vacancy for vacancy in self.vacancies_list if vacancy not in set(list_to_delete)]
                        self.vacancies_list = new_list

    @staticmethod
    def _get_file_name(source_name):
        file_name = f"{source_name.replace(' ', '_')}_vacancies.json"
        project_root = os.path.dirname(os.path.abspath(__file__))
        path_to_file = os.path.join(project_root, "..", "data", file_name)
        return path_to_file

    def is_valid_criteria(self, criteria: dict) -> bool:
        """ метод проверки корректности критериев для получения и удаления вакансий"""
        source_keys = ['name', 'salary', 'created_at', 'url', 'requirement', 'schedule']
        # проверка, что ключи запроса есть среди параметров вакансий
        if criteria and isinstance(criteria, dict):
            if not all(key in source_keys for key in criteria):
                self.log_warning("Некорректные условия, таких параметров нет у вакансий")
                return False
            else:
                return True
        else:
            return False


if __name__ == "__main__":
    vac1 = Vacancy(**{'name': 'Middle Backend Developer (Python FastAPI + SQL)',
                      'salary': 210000,
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
                      'created_at': '2025-02-21T14:00:01+0300',
                      'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                      'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>. '
                                     'Умение структурно мыслить, а также разбивать проект на подзадачи. '
                                     'Опыт с другими языками программирования, например...',
                      'schedule': 'Полный день',
                      })
    vac3 = Vacancy(**{'name': "test3",
                      'salary': 0.03,
                      'currency': "RUR",
                      'created_at': "test_date3",
                      'url': "test_url3",
                      'requirement': "test_requirement3",
                      'schedule': "test_schedule3",
                      })
    vac4 = Vacancy(**{'name': "test4",
                      'salary': 0.04,
                      'currency': "RUR",
                      'created_at': "test_date4",
                      'url': "test_url4",
                      'requirement': "test_requirement4",
                      'schedule': "test_schedule4",
                      })

    operator1 = JsonOperator("HeadHunter", "https://hh.ru", [])

    print(f"вакансий в списке объекта: {len(operator1.vacancies_list)}")

    vac_list = [vac3, vac4, vac1, vac2]

    # operator1.add_vacancies(vac_list[2:])
    # operator1.add_vacancies(vac_list1)
    # find_vac = operator1.get_vacancy(3)
    # print(find_vac)

    print(f"вакансий в списке объекта: {len(operator1.vacancies_list)}")
    criteria1 = {'salary': 0.03}
    operator1.del_vacancies({"schedule": "Удаленная работа"})
