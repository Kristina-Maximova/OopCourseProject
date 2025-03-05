from datetime import datetime
from unittest.mock import patch

import pytest

from src.vacancy import Vacancy


def test_vacancy_init():
    """ Тест на работу конструктора с корректными данными"""
    vac_1 = Vacancy(**{'name': 'Python-разработчик',
                       'salary': 80000,
                       'currency': "RUR",
                       'created_at': '2025-02-21T14:00:01+0300',
                       'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                       'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.',
                       'schedule': 'Полный день',
                       'vac_id': 800
                       })
    assert vac_1.name == 'Python-разработчик'
    assert vac_1.salary == 80000
    assert vac_1.currency == "RUR"
    assert vac_1.created_at == '2025-02-21T14:00:01+0300'
    assert vac_1.url == 'https://api.hh.ru/vacancies/116455408?host=hh.ru'
    assert vac_1.requirement == 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.'
    assert vac_1.schedule == 'Полный день'
    assert vac_1.vac_id == 800


def test_vacancy_comparisons(test_vacancy1, test_vacancy2, test_dict_vacancy1):
    """ Проверка работы магических методов сравнения
    и метода __hash__ (применяется в ф-ции set())"""
    assert test_vacancy1 > test_vacancy2
    assert test_vacancy1 >= test_vacancy2
    assert test_vacancy2 <= test_vacancy1
    assert test_vacancy2 < test_vacancy1
    assert test_vacancy1 != test_vacancy2
    assert test_vacancy2 == 80000
    list_with_vacs = [test_vacancy1, test_vacancy2]
    assert test_vacancy1 in set(list_with_vacs)
    with pytest.raises(TypeError) as exc_info:
        print(test_vacancy1 != test_dict_vacancy1)
        assert str(exc_info) == "Сравнение возможно только с объектом класса Vacancy или с числом"


def test_vacancy_str(test_vacancy2):
    """ Проверка работы магического метода __str__"""
    assert str(test_vacancy2) == ('801: Python-разработчик, зарплата 80000, url: '
                                  'https://api.hh.ru/vacancies/116455408?host=hh.ru.')


@patch("src.vacancy.get_usd_rate", return_value=1.5625)
def test_vacancy_usd_salary(mock_get):
    """ Тест на вызов метода конвертации зарплаты
     при инициализации данных с зарплатой в USD"""
    vac_usd = Vacancy(**{'name': 'Python',
                         'salary': 80000,
                         'currency': "USD",
                         'created_at': '2025-02-21T14:00:01+0300',
                         'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                         'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.',
                         'schedule': 'Полный день',
                         'vac_id': 801
                         })
    assert vac_usd.salary == 125000.0
    assert vac_usd.currency == "RUR"
    mock_get.assert_called_once()


def test_vacancy_invalid_date(test_vacancy_wrong_date_dict):
    """ Проверка, что дата или ISO - строка  или None """
    vac_no_date = Vacancy(**test_vacancy_wrong_date_dict)
    assert vac_no_date.created_at is None


def test_vacancy_to_dict(test_vacancy2):
    """ Проверка метода преобразования в словарь"""
    assert test_vacancy2.to_dict == {'created_at': '2025-02-21T14:00:01+0300',
                                     'currency': 'RUR',
                                     'name': 'Python-разработчик',
                                     'requirement': 'От 1 года коммерческой '
                                                    '<highlighttext>разработки</highlighttext>.',
                                     'salary': 80000,
                                     'schedule': 'Полный день',
                                     'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                                     'vac_id': 801}


def test_cast_to_object_list(test_dict_vacancy1,
                             test_dict_vacancy2,
                             test_vacancy1,
                             test_vacancy2):
    """ Проверка работы метода преобразования
     списка словарей в список объектов класса Vacancy"""
    dict_vacs_list = [test_dict_vacancy1, test_dict_vacancy2]
    obj_vacs_list = Vacancy.cast_to_object_list(dict_vacs_list)
    assert obj_vacs_list == [test_vacancy1, test_vacancy2]


def test_date_converting(test_vacancy1):
    """ Проверка методов преобразования параметра created_at"""
    test_vacancy1.to_datetime()
    assert type(test_vacancy1.created_at) is datetime
    test_vacancy1.to_iso_str()
    assert test_vacancy1.created_at == '2025-02-21T14:46:49+03:00'
