from abc import ABC, abstractmethod

import requests


class BaseApi(ABC):
    """
    Абстрактный класс для работы с API сервисом hh.ru.
    """

    @abstractmethod
    def get_info(self) -> None | list:
        """
        Абстрактный метод для получения списка вакансий по id работодателя с сайта hh.ru.
        """
        pass


class EmployersApi(BaseApi):
    """
    Класс для подключения к API hh.ru и получения данных о работодателе.
    """

    employers_url: str
    employers: list

    def __init__(self, employers_ids: list) -> None:
        """
        Метод-конструктор класса.
        """

        self.employers_url = "https://api.hh.ru/employers/"
        self.headers = {"User-Agent": "MyUniqueHHParserApp/1.0 (m10021994r@gmail.com)"}
        self.employers_ids = employers_ids
        self.employers = []

    def get_info(self) -> list:
        """
        Метод, получающий информацию о конкретном работодателе.
        """

        self.employers = []
        for employer_id in self.employers_ids:
            response = requests.get(f"{self.employers_url}/{employer_id}", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                self.employers.append({"id": result.get("id"), "name": result.get("name")})
        return self.employers


class VacanciesApi(BaseApi):
    """
    Класс для подключения к API и получения вакансий по id работодателя.
    """

    vacancies_url: str
    vacancies: list

    def __init__(self, employers_ids: list) -> None:
        """
        Метод-конструктор класса.
        """

        self.vacancies_url = "https://api.hh.ru/vacancies/"
        self.headers = {"User-Agent": "MyUniqueHHParserApp/1.0 (m10021994r@gmail.com)"}
        self.employers_ids = employers_ids
        self.vacancies = []

    def get_info(self) -> list:
        """
        Метод, получающий список вакансий по id работодателя.
        """
        self.vacancies = []

        for employer_id in self.employers_ids:
            response = requests.get(
                self.vacancies_url, headers=self.headers, params={"employer_id": employer_id, "per_page": 100}
            )
            if response.status_code == 200:
                result = response.json().get("items", [])
                for item in result:
                    self.vacancies.append(
                        {
                            "vacancy_id": item.get("id"),
                            "vacancy_name": item.get("name"),
                            "area": item.get("area")["name"],
                            "salary_from": item.get("from"),
                            "salary_to": item.get("to"),
                            "currency": item.get("currency"),
                            "type": item.get("typy")["name"],
                            "created_at": item.get("created_at"),
                            "updated_at": item.get("updated_at"),
                            "archived": item.get("archived"),
                            "employer_id": item.get("employer_id"),
                            "requirement": item.get("requirement"),
                            "responsibility": item.get("responsibility"),
                            "alternate_url": item.get("alternate_url"),
                            "experience_id": item.get("experience_id"),
                            "experience_name": item.get("experience_name"),
                            "employment_id": item.get("employment_id"),
                            "employment_name": item.get("employment_name"),
                            "schedule_id": item.get("schedule_id"),
                            "schedule_name": item.get("schedule_name"),
                        }
                    )
        return self.vacancies
