import json
from src.operator_abstract import VacanciesOperator
from src.vacancy import Vacancy


class JsonOperator(VacanciesOperator):
    """ Класс для сохранения информации о вакансиях в JSON-файл """

    def __init__(self, source_name: str, source_url: str, vacancies_list: list, file_path: str = ""):
        """ Конструктор класса для обработки данных с вакансиями и записи их в json-файл """
        self.source_name = source_name
        self.source_url = source_url
        self.__file_path = file_path if file_path else f"..\\data\\{source_name.replace(' ', '_')}_vacancies.json"
        self.vacancies_list = vacancies_list if vacancies_list else []

    # Методы __enter__ и __exit__ позволяют создать контекстный менеджер для работы с json-файлом
    def __enter__(self):
        """ Метод для получения данных о вакансиях из json-файла"""
        try:
            with open(self.__file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.__file_path} не найден и будет создан заново")
        except json.decoder.JSONDecodeError:  # например, если файл пустой, будет такая ошибка
            print(f"Ошибка получения данных из файла {self.__file_path}")
        else:
            if data:
                try:
                    for vacancy in data:
                        if Vacancy(**vacancy) not in self.vacancies_list:
                            self.vacancies_list.append(Vacancy(**vacancy))
                    # return self.vacancies_list
                except TypeError as e:
                    print(f"Данные в файле не читаются как вакансии: {e}")
        finally:
            print(f"в базе вакансий было: {len(self.vacancies_list)}")
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
                print("Ошибка, данные не записаны в файл")
            else:
                print(f"в базе вакансий стало: {len(self.vacancies_list)}")
        else:
            print("Нет данных для записи")

    def add_vacancy(self, new_vacancy):
        """ Добавляет объект класса Vacancy  в json-файл"""
        with self:
            if isinstance(new_vacancy, Vacancy) and not new_vacancy in self.vacancies_list:
                self.vacancies_list.append(new_vacancy)

    def get_vacancy(self, vac_id: int) -> None | Vacancy:
        """ Получает объект класса Vacancy из json-файла"""
        with self:
            for vacancy in self.vacancies_list:
                if vacancy.vac_id == vac_id:
                    return vacancy

    def del_vacancy(self, unwanted_vacancy):
        with self:
            if unwanted_vacancy in  self.vacancies_list:
                self.vacancies_list.remove(unwanted_vacancy)

    def add_vacancies(self, vacancies: list):
        """ Метод добавления списка объектов класса Vacancy в json-файл"""
        if vacancies:
            with self:
                try:
                    for vacancy in vacancies:
                        if not isinstance(vacancy, Vacancy):
                            raise TypeError("Внести в базу можно только объект класса Vacancy")
                        elif vacancy not in self.vacancies_list:
                            self.vacancies_list.append(vacancy)
                except Exception as e:
                    print(f"Вакансии не добавлены в файл, ошибка {e}")

    def get_vacancies(self, criteria: dict) -> list | None:
        """ Метод для получения из json-файла вакансий с заданными критериями
         criteria: параметр и его значение у вакансий, которые надо получить.
         Возвращает список вакансий, соответствующий критериям
         """
        with self:
            filtered_vacancies = []
            source_keys = ['name', 'salary', 'created_at', 'url', 'requirement', 'schedule']
            # проверка, что ключи запроса есть среди параметров вакансий
            if not all(key in source_keys for key in criteria):
                print("Некорректные условия, таких параметров нет у вакансий")
            else:
                if len(self.vacancies_list) > 0:
                    for key, value in criteria.items():
                        filtered_vacancies = [vacancy for vacancy in self.vacancies_list if
                                              getattr(vacancy, key) == value]
                print(f"найдено таких вакансий: {len(filtered_vacancies)}")
                return filtered_vacancies

    def del_vacancies(self, vacancies: list):
        """ Метод для удаления нескольких вакансий из json-файла """
        with self:
            if len(self.vacancies_list) > 0:
                data = []
                if vacancies:
                    for vacancy in vacancies:
                        if not isinstance(vacancy, Vacancy):
                            raise TypeError("Удалить можно только объект класса Vacancy")
                        elif vacancy in self.vacancies_list:
                            self.vacancies_list.remove(vacancy)


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

    vac_to_json1 = JsonOperator("HeadHunter", "https://hh.ru", [vac1, vac2])

    print(f"вакансий в списке объекта: {len(vac_to_json1.vacancies_list)}")

    # vac_to_json1.add_vacancy(vac3)
    vac_to_json1.add_vacancies([vac3, vac4])


    vac_to_json1.del_vacancy(vac3)


    # result = vac_to_json1.get_vacancies({'name': "test4"})
    # print(*result)

    # vac_to_json1.add_vacancies([vac3])
    # print(f"вакансий в списке объекта: {len(vac_to_json1.vacancies_list)}")

    # my_wanted_vacancies = vac_to_json1.get_vacancies({'salary': 80000})
    # print(len(my_wanted_vacancies))

    # vac_to_json1.del_vacancies([vac3])
    # print(f"вакансий в списке объекта: {len(vac_to_json1.vacancies_list)}")

    # vac_to_json1.add_vacancies([vac3])
    # print(f"вакансий в списке объекта: {len(vac_to_json1.vacancies_list)}")
