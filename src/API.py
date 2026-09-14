from abc import ABC, abstractmethod

import requests


class BaseApi(ABC):
    """
    Абстрактный класс для работы с API сервисом hh.ru.
    """

    @abstractmethod
    def get_vacancies(self) -> None:
        """
        Абстрактный метод для получения списка вакансий по id работодателя с сайта hh.ru.
        """
        pass


class EmployersApi:
    """
    Класс для подключения к API hh.ru и получения данных о работодателе.
    """

    employers_url: str
    employers: None | list

    def __init__(self) -> None:
        """
        Метод-конструктор класса.
        """

        self.employers_url = "https://api.hh.ru/employers"
        self.employers = None  # список словарей формата {"id": 123, "name": "Yandex"} с работодателями

    def get_employers(self) -> None:
        """
        Метод, получающий информацию о конкретном работодателе.
        """

        response = requests.get(
            self.employers_url, headers={"User-Agent": "MyUniqueHHParserApp/1.0 (m10021994r@gmail.com)"}
        )
        if response.status_code == 200:
            result = response.json()
            employers_info = result["items"]
            employers_info_valid = []
            for employer in employers_info:
                employers_info_valid.append({"id": employer["id"], "name": employer["name"]})
            self.employers = employers_info_valid  # employers_info_valid = [{"id": employer["id"], "name": employer["name"]} for employer in response.json()["items]]


class VacanciesApi(BaseApi):
    """
    Класс для подключения к API и получения id работодателей и открытых вакансиях,
    размещенных на сайте hh.ru.
    """

    vacancies_url: str
    vacancies: None | dict

    def __init__(self) -> None:
        """
        Метод-конструктор класса.
        """

        self.vacancies_url = "https://api.hh.ru/vacancies"
        self.vacancies = None  # список словарей с вакансиями

    def get_vacancies(self) -> None:
        """
        Метод, получающий список вакансий по id работодателя.
        """

        response = requests.get(
            self.vacancies_url, headers={"User-Agent": "MyUniqueHHParserApp/1.0 (m10021994r@gmail.com)"}
        )
        if response.status_code == 200:
            self.vacancies = response.json()["items"]
