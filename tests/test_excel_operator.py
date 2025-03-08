from src.excel_operator import ExcelOperator
from unittest.mock import patch
import pandas as pd


def test_excel_operator_init(test_vacancy1, test_vacancy2):
    """ Проверка работы конструктора класса ExcelOperator """
    operator = ExcelOperator("test_name",
                             "test_url",
                             [test_vacancy1, test_vacancy2],
                             "fake_file_path")
    assert operator.source_name == "test_name"
    assert operator.source_url == "test_url"
    assert operator.vacancies_list[0] == test_vacancy1
    assert operator.file_path == "fake_file_path"


@patch("pandas.DataFrame.to_excel", return_value=None)
@patch("pandas.read_excel", return_value=pd.DataFrame())
@patch.object(ExcelOperator, '__exit__', return_value=None)
def test_excel_operator_enter(mock_exit, mock_read_excel, mock_to_excel):
    """ Проверка работы магического метода
    для считывания данных о вакансиях из excel- файла"""
    operator = ExcelOperator("fake_name", "fake_url", [], "fake_file_path")
    with operator:
        operator.source_name = "fake_name1"
    assert len(operator.vacancies_list) == 0
    mock_read_excel.assert_called_with("fake_file_path", sheet_name='sheet_1')
    mock_exit.assert_called()
    mock_to_excel.assert_called()


@patch.object(ExcelOperator, '__enter__', return_value=None)
@patch("openpyxl.workbook.workbook.Workbook.save", return_value=None)
def test_excel_operator_exit(mock_save,
                             mock_enter,
                             test_vacancy1,
                             test_vacancy2):
    operator = ExcelOperator("fake_name",
                             "fake_url",
                             [test_vacancy1, test_vacancy2],
                             "fake_file_path")
    with operator:
        operator.source_name = "fake_name1"
    mock_save.assert_called_with("fake_file_path")
    mock_enter.assert_called()


def test_excel_add_vacancies(test_vacancy1, test_vacancy2):
    operator = ExcelOperator("fake_name",
                             "fake_url",
                             [],
                             "fake_file_path")
    # Патчим методы __enter__ и __exit__,
    with patch.object(ExcelOperator, '__enter__', return_value=operator), \
            patch.object(ExcelOperator, '__exit__', return_value=None):
        operator.add_vacancies([test_vacancy1, test_vacancy2])
        assert len(operator.vacancies_list) == 2
