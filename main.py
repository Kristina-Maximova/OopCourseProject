from src.api_guide import HH
from src.processing import DateAnalyzer, SalaryAnalyzer
from src.user_survey import user_interaction
from src.vac_operator import JsonOperator
from src.vacancy import Vacancy


def main():
    # Получаем пользовательские настройки. В запросе ожидается слово 'вакансия' или 'работа'
    try:
        user_settings = user_interaction()  # {'keywords': 'python', 'top_n': 3, 'date_from': '28.02.25'}
        keywords = user_settings.get('keywords')
    except AttributeError:
        return None
    top_n = user_settings.get('top_n')
    date_from = user_settings.get('date_from')

    # поиск вакансий на платформе HeadHunter
    hh_searcher = HH()
    data_from_hh = hh_searcher.get_vacancies(keywords)

    # cоздание объектов Vacancy из данных
    user_vacancies = Vacancy.cast_to_object_list(data_from_hh)

    # фильтруем полученные данные по дате создания и сортируем по зарплате
    date_analyzer = DateAnalyzer(user_vacancies)
    actual_date_vacancies = date_analyzer.filter_vacancies(date_from)
    salary_analyzer = SalaryAnalyzer(actual_date_vacancies)
    sorted_vacancies = salary_analyzer.sort_vacancies()

    # формируем вывод топ-n в консоль:
    print(f"После обработки осталось вакансий: {len(sorted_vacancies)}")
    print('-' * 119)
    for vacancy in sorted_vacancies[0:top_n]:
        print(vacancy)

    # Вносим топ-n в базу (записываем в json-файл)
    json_base_operator = JsonOperator("HeadHunter", "https://hh.ru", [])
    json_base_operator.add_vacancies(sorted_vacancies[0:top_n])
    print('-' * 119)
    if len(sorted_vacancies[0:top_n]) > 0:
        print("Вакансии из топ списка внесены в базу")


if __name__ == "__main__":
    main()
