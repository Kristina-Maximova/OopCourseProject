import json
from unittest.mock import mock_open, patch
from src.vac_operator import JsonOperator


def test_operator_init(test_init_data_for_operator, test_vacancy1, test_vacancy2):
    """ Проверка работы конструктора с корректными данными """
    test_operator1 = JsonOperator(**test_init_data_for_operator)
    assert test_operator1.source_name == "HeadHunter"
    assert test_operator1.source_url == "https://hh.ru"
    assert test_operator1.vacancies_list == [test_vacancy1, test_vacancy2]
    assert test_operator1.file_path == "fake/file_path"


def test_path():
    """ Проверка работы геттера, сеттера и метода """
    test_operator2 = JsonOperator("HH", "hh.ru", [])
    test_operator2.file_path = "Fake/path"
    assert test_operator2.file_path == "Fake/path"


def test_enter_method():
    """ проверка работы магического метода __enter__ """
    mock_data = json.dumps([{
        "name": "test3",
        "salary": 0.03,
        "currency": "RUR",
        "created_at": None,
        "url": "test_url3",
        "requirement": "test_requirement3",
        "schedule": "test_schedule3",
        "vac_id": 3
    }])
    # Создаем mock для open
    m = mock_open(read_data=mock_data)
    # Патч для функции open
    with patch('builtins.open', m):
        operator = JsonOperator('source_name', 'source_url', [], file_path="fake_path")
        with operator:
            assert len(operator.vacancies_list) == 1
    m.assert_called_with("fake_path", "w+", encoding='utf-8')
    handle = m()
    handle.read.assert_called()


def test_exit_method(test_vacancy1):
    """ проверка работы магического метода __exit__ """
    data_to_write = [{
        "name": "test3",
        "salary": 0.03,
        "currency": "RUR",
        "created_at": None,
        "url": "test_url3",
        "requirement": "test_requirement3",
        "schedule": "test_schedule3",
        "vac_id": 3
    }]
    # Создаем mock для open
    m = mock_open()
    # Патч для функции open
    with patch('builtins.open', m):
        operator = JsonOperator('source_name', 'source_url', [test_vacancy1], file_path="fake_path")
        with operator:
            operator.data = data_to_write
    m.assert_called_with("fake_path", "w+", encoding='utf-8')
    handle = m()
    handle.write.assert_called()


def test_add_get_del_vacancy(test_vacancy1, test_vacancy2):
    """ Проверка методов получения, добавления и удаления одной вакансии """
    operator = JsonOperator("HeadHunter", "https://hh.ru", [test_vacancy1], file_path="Fake_path")
    # Патчим методы __enter__ и __exit__, которые вызываются при использовании контекстного менеджера
    with patch.object(JsonOperator, '__enter__', return_value=operator), \
            patch.object(JsonOperator, '__exit__', return_value=None):
        vac_1 = operator.get_vacancy(800)
        assert vac_1.name == 'Middle Backend Developer (Python FastAPI + SQL)'
        operator.add_vacancy(test_vacancy2)
        assert operator.vacancies_list == [test_vacancy1, test_vacancy2]
        operator.del_vacancy(test_vacancy1)
        assert operator.vacancies_list == [test_vacancy2]


def test_add_get_del_vacancies(test_vacancy1, test_vacancy2):
    """ Проверка методов работы с несколькими вакансиями"""
    operator = JsonOperator("HeadHunter", "https://hh.ru", [], file_path="Fake_path")
    # Патчим методы __enter__ и __exit__, которые вызываются при использовании контекстного менеджера
    with patch.object(JsonOperator, '__enter__', return_value=operator), \
            patch.object(JsonOperator, '__exit__', return_value=None):
        operator.add_vacancies([test_vacancy1, test_vacancy2])
        assert operator.vacancies_list == [test_vacancy1, test_vacancy2]
        criteria = {'schedule': 'Удаленная работа'}
        search_list = operator.get_vacancies(criteria)
        assert search_list == [test_vacancy1]
        operator.del_vacancies(criteria)
        assert operator.vacancies_list == [test_vacancy2]


if __name__ == '__main__':
    pass
