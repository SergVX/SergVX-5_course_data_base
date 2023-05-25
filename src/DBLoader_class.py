import psycopg2


class DB_Loader:
    """ Класс для загрузки данных в БД."""
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def create_employers(self) -> None:
        """
        Создание таблицы для ее последующего заполнения данными о работодателях.
        :return: None
        """
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute(f'CREATE TABLE "employers"'
                                f'(id integer PRIMARY KEY,'
                                f'name varchar,'
                                f'alternate_url varchar,'
                                f'open_vacancies integer);')

        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def create_vacancies(self) -> None:
        """
        Создание таблицы для ее последующего заполнения данными о вакансиях.
        :return: None
        """
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    cur.execute(f'CREATE TABLE "vacancies"'
                                f'(id integer PRIMARY KEY,'
                                f'name varchar,'
                                f'salary_min integer,'
                                f'salary_max integer,'
                                f'currency varchar,'
                                f'alternate_url varchar,'
                                f'employer_id integer REFERENCES employers(id) NOT NULL,'
                                f'requirement varchar,'
                                f'responsibility varchar);')

        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def fill_employers(self, employers_list):
        """
        Заполняет таблицу в базе данных Postgres из списка словарей
        param: table_name: Название таблицы в БД
        param: employers_list: Список работодателей
        """
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    print("Успешное подключение к базе данных.")
                    for data in employers_list:
                        cur.execute(
                            f"INSERT INTO employers (id, name, alternate_url, open_vacancies) VALUES (%s, %s, %s,"
                            f" %s)", (data['id'], data['name'], data['alternate_url'], data['open_vacancies'])
                        )
                    connection.commit()
                    print("Данные успешно внесены в таблицу employers.")
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def fill_vacancies(self, vacancies_list):
        """
        Заполняет таблицу в базе данных Postgres из списка вакансий
        param: table_name: Название таблицы в БД
        param: vacancies_list: Список вакансий
        """
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    print("Успешное подключение к базе данных.")
                    for data in vacancies_list:
                        cur.execute(
                            f"INSERT INTO vacancies (id, name, alternate_url, salary_min, salary_max, currency,"
                            f"employer_id, requirement, responsibility) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (data['id'], data['name'], data['alternate_url'], data['salary_min'], data['salary_max'],
                             data['currency'], data['employer_id'], data['requirement'], data['responsibility'])
                        )
                    connection.commit()
                    print("Данные успешно внесены в таблицу vacancies.")
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def delete_employers(self):
        """Удаляет данные из таблицы employers"""
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    print("Успешное подключение к базе данных.")
                    cur.execute("delete from employers")
                    connection.commit()
                    print("Данные из таблицы employers успешно удалены.")
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def delete_vacancies(self):
        """Удаляет данные из таблицы vacancies"""
        try:
            with psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cur:
                    print("Успешное подключение к базе данных.")
                    cur.execute("delete from vacancies")
                    connection.commit()
                    print("Данные из таблицы vacancies успешно удалены.")
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)

    def delete_all(self):
        """Удаляет данные из таблиц employers и vacancy"""
        self.delete_vacancies()
        self.delete_employers()
