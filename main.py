from src.API import EmployersApi, VacanciesApi
from src.CreateDB import create_database, create_tables, insert_data_from_api, insert_data_from_file
from src.DBManager import DBManager
from src.File_manager import open_file_manager

employers_ids = ["1740", "15478", "2460946", "4233", "4181", "2120", "3529", "1373", "766468", "39305"]


def main() -> None:
    """
    Основная функция, объединяющая все классы и функции в единую программу.
    """

    create_database()
    create_tables()

    employers = EmployersApi(employers_ids)
    employers_data = employers.get_info()
    vacancies = VacanciesApi(employers_ids)
    vacancies_data = vacancies.get_info()

    database = DBManager()

    if employers_data and vacancies_data:
        insert_data_from_api(employers_data, vacancies_data)
    else:
        data = open_file_manager("data/hh_vacancies.json")
        insert_data_from_file(data)

    while True:
        print("=" * 62)
        print("Выберете пункт МЕНЮ для вывода следующей информации".center(62))
        print("=" * 62)
        print()
        print("1. Список компаний и количество доступных вакансий.")
        print("2. Список вакансий с указанием названия компании, заработной платы и ссылки на вакансию.")
        print("3. Средняя заработная плата по вакансиям.")
        print("4. Список вакансий, заработная плата которых выше средней по рынку.")
        print("5. Поиск вакансий, по ключевым словам.")
        print("0. Для выхода из программы.")
        print()

        user_option = input(">>> ")
        print()
        if user_option == "1":
            result = database.get_companies_and_vacancies_count()
            for employer in result:
                print(f"Компания: {employer[0]} | Количество вакансий: {employer[1]}")
            print()
        if user_option == "2":
            result = database.get_all_vacancies()
            for employer in result:
                print(
                    f"Компания: {employer[0]} | Вакансия: {employer[1]} | Диапазон: {employer[2]} | "
                    f"Ссылка на вакансию: {employer[3]}"
                )
            print()
        if user_option == "3":
            result = database.get_avg_salary()
            for vacancy in result:
                print(f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Средняя: {vacancy[2]}")
            print()
        if user_option == "4":
            result = database.get_vacancies_with_higher_salary()
            global_avg_sum = round(result[0][4])
            print(f"--- Фильтрация идет относительно средней зарплаты по рынку: {global_avg_sum} руб. ---\n")
            for vacancy in result:
                print(
                    f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Диапазон: {vacancy[2]} "
                    f"(Средняя: {round(vacancy[3])} руб.)"
                )
            print()
        if user_option == "5":
            user_input = input("Введите слова для поиска через запятую: ").lower().split(",")
            print()
            result = database.get_vacancies_with_keyword(user_input)
            for vacancy in result:
                print(f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Диапазон: {vacancy[2]}")
            print()
        if user_option == "0":
            break


main()
