import psycopg2


class DB_Manager:
    """ Класс для работы с данными в БД."""
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список данных
        """

        info = None

        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute("SELECT name, open_vacancies FROM employers")
                    info = cur.fetchall()
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            if connection:
                connection.close()

        return info

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return: Список данных
        """
        info = None

        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute("select e.name, v.name, salary_min, salary_max, currency, v.alternate_url  from vacancies v "
                                "join employers e on e.id = v.employer_id "
                                "order by e.name")
                    info = cur.fetchall()
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            if connection:
                connection.close()

        return info

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: Список данных
        """
        info = None

        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "select AVG(salary_min) as salary_min, AVG(salary_max) as salary_max from "
                        "vacancies v ")
                    info = cur.fetchone()
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            if connection:
                connection.close()

        return info

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Список данных
        """
        info = None

        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "select * from vacancies v "
                        "where salary_min > (select avg(salary_min) from vacancies v2) "
                        "order by salary_min desc ")
                    info = cur.fetchall()
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            if connection:
                connection.close()

        return info

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        :param keyword:
        :return: Список данных
        """
        info = None

        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "select * from vacancies v "
                        f"where name ilike '%{keyword}%'")
                    info = cur.fetchall()
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            if connection:
                connection.close()

        return info
