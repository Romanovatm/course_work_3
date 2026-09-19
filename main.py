from src.API import EmployersApi, VacanciesApi
from src.CreateDB import create_database, create_tables, insert_data
from src.DBManager import DBManager
from src.File_manager import file_manager


def main() -> None:
    """
    Основная функция, объединяющая все классы и функции в единую программу.
    """

    create_database()
    create_tables()

    employers = EmployersApi()
    employers.get_employers()
    vacancies = VacanciesApi()
    vacancies.get_vacancies()

    if not employers.employers and not vacancies.vacancies:
        data = file_manager("data/hh_vacancies.json")
        insert_data(data)
    else:
        insert_data(vacancies.vacancies)  # type: ignore

    while True:
        print("Выберете пункт МЕНЮ для вывода следующей информации:")
        print("1. Список компаний и количество доступных вакансий.")
        print("2. Список вакансий с указанием названия компании, заработной платы и ссылки на вакансию.")
        print("3. Средняя заработная плата по вакансиям.")
        print("4. Список вакансий, заработная плата которых выше средней по рынку.")
        print("5. Поиск вакансий, по ключевым словам.")
        print("0. Для выхода из программы.")

        user_option = input()
        if user_option == "1":
            DBManager.get_companies_and_vacancies_count()
        if user_option == "2":
            DBManager.get_all_vacancies()
        if user_option == "3":
            DBManager.get_avg_salary()
        if user_option == "4":
            DBManager.get_vacancies_with_higher_salary()
        if user_option == "5":
            user_input = input("Введите слова для поиска через запятую: ").lower().split()
            DBManager.get_vacancies_with_keyword(user_input)
        if user_option == "0":
            break


main()
