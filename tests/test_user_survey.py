from unittest.mock import patch
from src.user_survey import (is_valid_date_from,
                             is_valid_top_n, is_valid_words,
                             user_interaction)


@patch("builtins.input", side_effect=["вакансия", "Python", "3", "03.03.25"])
def test_user_interaction(mock_input):
    """ Проверка метода формирования запроса с пользовательским вводом"""
    result = user_interaction()
    assert result == {'date_from': '03.03.25', 'keywords': 'Python', 'top_n': 3}


def test_is_valid_methods():
    """ Проверка методов валидации вводимых пользователем данных"""
    assert is_valid_words("words Words, words!") is True
    assert is_valid_words("11, 12, ") is False
    assert is_valid_top_n("1") is True
    assert is_valid_top_n("два") is False
    assert is_valid_date_from("03.03.25") is True
    assert is_valid_date_from("03.03.30") is False
    assert is_valid_date_from("2025-03-03") is False
