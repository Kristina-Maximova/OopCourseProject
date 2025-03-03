import pytest
from src.vacancy import Vacancy


@pytest.fixture
def test_vacancy1():
    return Vacancy(**{'name': 'Middle Backend Developer (Python FastAPI + SQL)',
                      'salary': 210000,
                      'currency': "RUR",
                      'created_at': '2025-02-21T14:46:49+0300',
                      'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
                      'requirement': 'Написание качественного кода и тестов к нему.',
                      'schedule': 'Удаленная работа',
                      'vac_id': 800
                      })


@pytest.fixture
def test_vacancy2():
    return Vacancy(**{'name': 'Python-разработчик',
                      'salary': 80000,
                      'currency': "RUR",
                      'created_at': '2025-02-21T14:00:01+0300',
                      'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
                      'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.',
                      'schedule': 'Полный день',
                      'vac_id': 801
                      })


@pytest.fixture
def test_vacancy3():
    return Vacancy(**{
        "name": "Fullstack developer (Python)",
        "salary": 300000,
        "currency": "RUR",
        "created_at": "2025-03-03T11:32:15+03:00",
        "url": "https://api.hh.ru/vacancies/117468876?host=hh.ru",
        "requirement": "Отличное владение каким-либо backend-стеком технологий (<highlighttext>Python</highlighttext>, Java, Go и т.п.). Достаточное :) владение react. Готовность освоить наш стек...",
        "schedule": "Удаленная работа",
        "vac_id": 56
    })


@pytest.fixture
def test_vacancy_wrong_date_dict():
    return {'name': 'Python-разработчик',
            'salary': 80000,
            'currency': "RUR",
            'created_at': 'wrong_date',
            'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
            'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.',
            'schedule': 'Полный день',
            'vac_id': 801
            }


@pytest.fixture
def test_dict_vacancy1():
    return {'name': 'Middle Backend Developer (Python FastAPI + SQL)',
            'salary': 210000,
            'currency': "RUR",
            'created_at': '2025-02-21T14:46:49+0300',
            'url': 'https://api.hh.ru/vacancies/117570423?host=hh.ru',
            'requirement': 'Написание качественного кода и тестов к нему.',
            'schedule': 'Удаленная работа',
            'vac_id': 800
            }


@pytest.fixture
def test_dict_vacancy2():
    return {'name': 'Python-разработчик',
            'salary': 80000,
            'currency': "RUR",
            'created_at': '2025-02-21T14:00:01+0300',
            'url': 'https://api.hh.ru/vacancies/116455408?host=hh.ru',
            'requirement': 'От 1 года коммерческой <highlighttext>разработки</highlighttext>.',
            'schedule': 'Полный день',
            'vac_id': 801
            }


@pytest.fixture
def test_init_data_for_operator(test_vacancy1, test_vacancy2):
    return {"source_name": "HeadHunter",
            "source_url": "https://hh.ru",
            "vacancies_list": [test_vacancy1, test_vacancy2],
            "file_path": "fake/file_path"}


@pytest.fixture
def hh_response():
    return {'items': [{'id': '117308260',
                       'name': 'Junior Python разработчик',
                       'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
                       'salary': {'from': None, 'to': 80000, 'currency': 'RUR', 'gross': False},
                       'created_at': '2025-03-03T16:45:05+0300',
                       'url': 'https://api.hh.ru/vacancies/117308260?host=hh.ru',
                       'employer': {'id': '5155838', 'name': 'Андреев Артём Александрович',
                                    'url': 'https://api.hh.ru/employers/5155838',
                                    'alternate_url': 'https://hh.ru/employer/5155838',
                                    'logo_urls': {'240': 'https://img.hhcdn.ru/employer-logo/6705035.png',
                                                  'original': 'https://img.hhcdn.ru/employer-logo-original/1271181.png',
                                                  '90': 'https://img.hhcdn.ru/employer-logo/6705034.png'},
                                    'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=5155838',
                                    'accredited_it_employer': False,
                                    'trusted': True},
                       'snippet': {
                           'requirement': 'Умение работать по Scrum, работа в таск-трекере. Навыки написания тестов. <highlighttext>Python</highlighttext> 3.11. Asyncio. FastApi (Pydantic v2). MongoDB. ',
                           'responsibility': 'Разработка нового функционала совместно с командой. Поддержка кодовой базы в актуальном состоянии. Участие в Code Review. Исправление багов.'},
                       'contacts': None,
                       'schedule': {'id': 'remote', 'name': 'Удаленная работа'}
                       }
                      ],
            'pages': 0}
