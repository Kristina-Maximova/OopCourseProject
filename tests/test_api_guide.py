from unittest.mock import patch

from src.api_guide import HH


def test_hh_init():
    """ Проверка работы конструктора класса"""
    hh_guide = HH()
    assert hh_guide.url == 'https://api.hh.ru/vacancies'
    assert hh_guide.headers == {'HH-User-Agent': 'OopCourseProject (e-mail)'}
    assert hh_guide.params['only_with_salary'] is True


@patch("requests.get")
def test_may_connect(mock_get):
    """ Проверка работы метода may_connect при успешном соединении  """
    hh_guide = HH()
    mock_get.return_value.status_code = 200
    assert hh_guide._ApiExplorer__may_connect() is True


@patch("requests.get")
def test_no_may_connect(mock_get):
    hh_guide = HH()
    mock_get.return_value.status_code = 400
    assert hh_guide._ApiExplorer__may_connect() is False


@patch("requests.get")
def test_get_vacancies(mock_get, hh_response):
    hh_guide = HH()
    mock_get.return_value.json.return_value = hh_response
    mock_get.return_value.status_code = 200
    vacancies_list = hh_guide.get_vacancies("fake words")
    assert vacancies_list[0] == {'created_at': '2025-03-03T16:45:05+0300',
                                 'currency': 'RUR',
                                 'name': 'Junior Python разработчик',
                                 'requirement': 'Умение работать по Scrum, работа в таск-трекере. Навыки '
                                                'написания тестов. <highlighttext>Python</highlighttext> 3.11. '
                                                'Asyncio. FastApi (Pydantic v2). MongoDB. ',
                                 'salary': None,
                                 'schedule': 'Удаленная работа',
                                 'url': 'https://api.hh.ru/vacancies/117308260?host=hh.ru'}
    mock_get.assert_called()
