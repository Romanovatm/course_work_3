import psycopg2

from src.CreateDB import password


class DBManager:
    """
    Класс для подключения к БД.
    """

    conn_params = {"host": "localhost", "database": "vacancies", "user": "postgres", "password": password}

    @staticmethod
    def get_companies_and_vacancies_count() -> None:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name, COUNT(vacancies.vacancy_id) FROM vacancies
                JOIN employers USING(employer_id)
                GROUP BY employers.employer_name
                """)
                total_vacancies_from_employers = cur.fetchall()
                for employer in total_vacancies_from_employers:
                    print(f"Компания: {employer[0]} | Количество вакансий: {employer[1]}")

    @staticmethod
    def get_all_vacancies() -> None:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """

        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name, vacancies.vacancy_name,
                CONCAT(vacancies.salary_from, '-', vacancies.salary_to) AS salary,
                vacancies.alternate_url
                FROM vacancies
                JOIN employers USING(employer_id)
                ORDER BY employers.employer_name, vacancies.vacancy_name
                """)
                result = cur.fetchall()
                for employer in result:
                    print(
                        f"Компания: {employer[0]} | Вакансия: {employer[1]} | Диапазон: {employer[2]} | "
                        f"Ссылка на вакансию: {employer[3]}"
                    )

    @staticmethod
    def get_avg_salary() -> None:
        """
        Получает среднюю зарплату по вакансиям.
        """

        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name,
                vacancies.vacancy_name,
                (vacancies.salary_from + vacancies.salary_to)/2 AS average
                FROM vacancies
                JOIN employers USING(employer_id)
                """)
                average_salary = cur.fetchall()
                for vacancy in average_salary:
                    print(f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Средняя: {vacancy[2]}")

    @staticmethod
    def get_vacancies_with_higher_salary() -> None:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name, vacancies.vacancy_name,
                CONCAT(vacancies.salary_from, '-', vacancies.salary_to) AS salary,
                (vacancies.salary_from + vacancies.salary_to)/2 AS avg_salary,
                (SELECT AVG((vacancies.salary_from + vacancies.salary_to)/2) FROM vacancies) AS global_market_avg
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE (vacancies.salary_from + vacancies.salary_to)/2 >
                (SELECT AVG((salary_from + vacancies.salary_to) / 2) FROM vacancies);
                """)
                avg_salary = cur.fetchall()
                global_avg_sum = round(avg_salary[0][4])
                print(f"--- Фильтрация идет относительно средней зарплаты по рынку: {global_avg_sum} руб. ---\n")
                for vacancy in avg_salary:
                    print(
                        f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Диапазон: {vacancy[2]} "
                        f"(Средняя: {round(vacancy[3])} руб.)"
                    )

    @staticmethod
    def get_vacancies_with_keyword(user_input: list) -> None:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например python.
        """

        search_patterns = [f"%{word.strip()}%" for word in user_input if word.strip()]

        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                SELECT employers.employer_name,
                vacancies.vacancy_name,
                CONCAT(vacancies.salary_from, '-', vacancies.salary_to) AS salary
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE vacancies.vacancy_name ILIKE ANY(%s);
                """,
                    (search_patterns,),
                )
                filter_vacancies = cur.fetchall()
                for vacancy in filter_vacancies:
                    print(f"Компания: {vacancy[0]} | Вакансия: {vacancy[1]} | Диапазон: {vacancy[2]}")
