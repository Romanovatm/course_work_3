import psycopg2

from src.CreateDB import password


class DBManager:
    """
    Класс для подключения к БД.
    """

    def __init__(self) -> None:
        """
        Метод-конструктор класса.
        """

        self.conn_params = {"host": "localhost", "database": "vacancies", "user": "postgres", "password": password}

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name, COUNT(vacancies.vacancy_id) FROM vacancies
                JOIN employers USING(employer_id)
                GROUP BY employers.employer_name
                """)
                total_vacancies_from_employers = cur.fetchall()
                return list(total_vacancies_from_employers)

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """

        with psycopg2.connect(**self.conn_params) as conn:
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
                return list(result)

    def get_avg_salary(self) -> list:
        """
        Получает среднюю зарплату по вакансиям.
        """

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.employer_name,
                vacancies.vacancy_name,
                (vacancies.salary_from + vacancies.salary_to)/2 AS average
                FROM vacancies
                JOIN employers USING(employer_id)
                """)
                average_salary = cur.fetchall()
                return list(average_salary)

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        with psycopg2.connect(**self.conn_params) as conn:
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
                return list(avg_salary)

    def get_vacancies_with_keyword(self, user_input: list) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например python.
        """

        search_patterns = [f"%{word.strip()}%" for word in user_input if word.strip()]

        with psycopg2.connect(**self.conn_params) as conn:
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
                return list(filter_vacancies)
