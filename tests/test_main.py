from unittest.mock import patch

from main import main


@patch("main.JsonOperator.add_vacancies")
@patch("main.HH.get_vacancies")
@patch("main.user_interaction")
def test_main(mock_get1, mock_get2, mock_get3, capsys):
    mock_get1.return_value = {'keywords': 'python', 'top_n': 3, 'date_from': '28.02.25'}
    mock_get2.return_value = [{'name': 'Junior Python разработчик',
                               'salary': None,
                               'currency': 'RUR',
                               'created_at': '2025-03-03T16:45:05+0300',
                               'url': 'https://api.hh.ru/vacancies/117308260?host=hh.ru',
                               'requirement': 'Навыки написания тестов.',
                               'schedule': 'Удаленная работа'}]
    mock_get3.return_value = None
    main()
    message = capsys.readouterr()
    assert message.out == ('После обработки осталось вакансий: 1\n'
                           '-----------------------------------------------------'
                           '------------------------------------------------------------------\n'
                           '1: Junior Python разработчик, зарплата 0.0, url: '
                           'https://api.hh.ru/vacancies/117308260?host=hh.ru.\n'
                           '------------------------------------------------------'
                           '-----------------------------------------------------------------\n'
                           'Вакансии из топ списка внесены в базу\n')
