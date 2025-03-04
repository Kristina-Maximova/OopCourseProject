from src.processing import DateAnalyzer, SalaryAnalyzer


def test_salary_processing(test_vacancy1, test_vacancy2, test_vacancy3):
    """ Проверка работы методов сортировки и фильтрации класса SalaryAnalyzer"""
    vacancies = [test_vacancy1, test_vacancy2, test_vacancy3]
    salary_analyzer = SalaryAnalyzer(vacancies)
    salary_analyzer.sort_vacancies()
    assert salary_analyzer.vacancies[0] == test_vacancy3
    filtered_list = salary_analyzer.filter_vacancies(150000)
    assert filtered_list[1] == test_vacancy1


def test_date_processing(test_vacancy1, test_vacancy2, test_vacancy3):
    """ Проверка работы методов сортировки и фильтрации класса DateAnalyzer"""
    vacancies = [test_vacancy1, test_vacancy2, test_vacancy3]
    date_analyzer = DateAnalyzer(vacancies)
    date_analyzer.sort_vacancies()
    assert date_analyzer.vacancies[0] == test_vacancy3
    filtered_list = date_analyzer.filter_vacancies("01.03.25")
    assert filtered_list[0] == test_vacancy3
