import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("PASSWORD")


def create_database() -> None:
    """
    Функция для создания базы данных. Если база существует — подключается к ней.
    Если нет — создает её.
    """

    try:
        with closing(psycopg2.connect(host="localhost", database="vacancies", user="postgres", password=password)):
            pass
    except UnicodeDecodeError:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password=password)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute("CREATE DATABASE vacancies WITH ENCODING 'UTF8';")
        cur.close()
        conn.close()


def create_tables() -> None:
    """
    Функция для создания таблиц employers и vacancies в базе данных vacancies.
    """

    conn = psycopg2.connect(host="localhost", database="vacancies", user="postgres", password=password)
    conn.set_client_encoding("UTF8")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employers(
        employer_id int PRIMARY KEY,
        employer_name varchar(200) NOT NULL
        );
    CREATE TABLE IF NOT EXISTS vacancies(
        vacancy_id int PRIMARY KEY,
        vacancy_name varchar(100) NOT NULL,
        area varchar(100) NOT NULL,
        salary_from int NOT NULL,
        salary_to int NOT NULL,
        currency varchar(10) NOT NULL,
        type varchar(100) NOT NULL,
        created_at timestamp NOT NULL,
        published_at timestamp NOT NULL,
        archived boolean NOT NULL,
        employer_id int NOT NULL,
        requirement text NOT NULL,
        responsibility text NOT NULL,
        experience_id varchar(100) NOT NULL,
        experience_name varchar(100) NOT NULL,
        employment_id varchar(100) NOT NULL,
        employment_name varchar(100) NOT NULL,
        schedule_id varchar(100) NOT NULL,
        schedule_name varchar(100) NOT NULL,
    CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_data(data: dict) -> None:
    """
    Функция для заполнения данными таблицы employers и vacancies базы данных vacancies.
    """
    conn = psycopg2.connect(host="localhost", database="vacancies", user="postgres", password=password)
    conn.set_client_encoding("UTF8")
    cur = conn.cursor()

    for employer in data["items"]:
        cur.execute(
            """
            INSERT INTO employers(employer_id, employer_name)
            VALUES(%s, %s)
            ON CONFLICT (employer_id) DO NOTHING;
            """,
            (employer["employer"]["id"], employer["employer"]["name"]),
        )

    for vacancy in data["items"]:
        cur.execute(
            """
            INSERT INTO vacancies(vacancy_id, vacancy_name, area, salary_from, salary_to, currency, type, created_at, published_at, archived, employer_id, requirement, responsibility, experience_id, experience_name, employment_id, employment_name, schedule_id, schedule_name)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
            """,
            (
                vacancy["id"],
                vacancy["name"],
                vacancy["area"]["name"],
                vacancy["salary"]["from"],
                vacancy["salary"]["to"],
                vacancy["salary"]["currency"],
                vacancy["type"]["name"],
                vacancy["created_at"],
                vacancy["published_at"],
                vacancy["archived"],
                vacancy["employer"]["id"],
                vacancy["snippet"]["requirement"],
                vacancy["snippet"]["responsibility"],
                vacancy["experience"]["id"],
                vacancy["experience"]["name"],
                vacancy["employment"]["id"],
                vacancy["employment"]["name"],
                vacancy["schedule"]["id"],
                vacancy["schedule"]["name"],
            ),
        )
    conn.commit()
    cur.close()
    conn.close()
