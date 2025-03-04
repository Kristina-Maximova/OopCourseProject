from datetime import datetime


def user_interaction() -> dict | None:
    """ Функция взаимодействия с пользователем"""

    while True:
        # получаем запрос на поиск вакансий
        words_to_start_searching = ["вакансии", "вакансия", "вакансию", "работа", "работу"]
        search_query = input("Введите поисковый запрос: ")  # ожидаем ввод слов вакансия или работа
        word_match = list(word for word in words_to_start_searching if word in search_query.lower().split())
        if len(word_match) > 0:
            print("Рады будем помочь в поиске работы вашей мечты!")
            # запрос получен, уточняем параметры поиска
            counter = 0
            while counter < 3:
                keywords = input("Введите ключевые слова для фильтрации вакансий: ")
                top_n = input("Введите количество вакансий для вывода в топ N: ")
                date_from = input("Начиная с какой даты ищем вакансии?\n"
                                  "Введите дату в формате ДД.MM.ГГ: ")

                # проверяем корректность полученных параметров
                if (is_valid_words(keywords)
                        and is_valid_top_n(top_n)
                        and is_valid_date_from(date_from)):
                    return {"keywords": keywords, "top_n": int(top_n), "date_from": date_from}
                else:
                    counter += 1
                    print("Неверные данные для поиска. Попробуйте ввести снова, будьте внимательны.")
            print("Превышено количество попыток")
            break
        print("Нет запроса на поиск")
        break


def is_valid_words(user_keywords: str) -> bool:
    """ проверка, что строка содержит хотя бы одно слово"""
    check = list(word for word in user_keywords.split() if word.isalpha())
    if len(check) > 0:
        return True
    return False


def is_valid_top_n(user_top_n: str) -> bool:
    """проверка, что введено число"""
    try:
        int(user_top_n)
        return True
    except ValueError:
        return False


def is_valid_date_from(user_date_from: str) -> bool:
    """ Проверка, что введена дата в указанном формате,
     и что она не больше текущей даты"""
    try:
        dt_obj = datetime.strptime(user_date_from, "%d.%m.%y")
        dt_now = datetime.now()
        if dt_obj <= dt_now:
            return True
        return False
    except ValueError:
        return False


if __name__ == "__main__":  # pragma: no cover
    my_result = user_interaction()
    print(my_result)  # {'keywords': 'python', 'top_n': 3, 'date_from': '28.02.25'}
