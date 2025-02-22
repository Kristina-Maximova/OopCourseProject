class Vacancy():
    """ Класс для представления вакансии"""

    def __init__(self, name: str, salary: float | None, created_at: str, url: str, requirement: str, schedule: str):
        self.name = name
        self.salary = salary if salary is not None else 0.0
        self.created_at = created_at
        self.url = url
        self.requirement = requirement
        self.schedule = schedule

    def __str__(self):
        return f"{self.name}, зарплата {self.salary}."

    # @classmethod
    # def sort_by_salary(self):
    #     pass

    def compare_salaries(self, other):
        """ Метод сравнения вакансий по зарплате """
        try:
            if not hasattr(self, "salary") or not hasattr(other, "salary"):  # проверка на наличие ключа
                raise ValueError("Нет поля с зарплатой у одной из вакансий")
            if self.salary == 0.0 or other.salary == 0.0:  # проверка, что з/п указана
                raise ValueError("Не указана одна из зарплат")
        except ValueError as e:
            return (f"Сравнение некорректно: {e}")
        else:
            if self.salary == other.salary:
                return "equal"
            elif self.salary > other.salary:
                return "more"
            else:
                return "less"


if __name__ == "__main__":
    vac1 = Vacancy(**{'name': 'Middle Backend Developer (Python FastAPI + SQL)',
                    'salary': 215000,
                    'created_at': '2025-02-21T14:46:49+0300',
                    'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
                    'requirement': 'Написание качественного кода и тестов к нему. '
                                   'Необходимый стек: <highlighttext>Python</highlighttext> (asyncio), '
                                   'чистый SQL (не ORM), FastAPI (весь функционал), микросервисная архитектура...',
                    'schedule': 'Удаленная работа'})
    vac2 = Vacancy(**{'name': 'Python-разработчик',
                    'salary': 80000,
                    'created_at': '2025-02-21T14:00:01+0300',
                    'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                    'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>. '
                                   'Умение структурно мыслить, а также разбивать проект на подзадачи. '
                                   'Опыт с другими языками программирования, например...',
                    'schedule': 'Полный день'})
    print(vac1)
    print(vac2)
    result = vac1.compare_salaries(vac2)
    print(result)