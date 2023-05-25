from src.DBLoader_class import DB_Loader
from src.DBManager import DB_Manager
from src.api_class import HH_api
from src.utils import get_user_answer, get_employers_id, get_formatted_vacancy

if __name__ == '__main__':

    host = "localhost"
    database = "5_course_data"
    user = "postgres"
    password = None
    employers_data = None
    vacancies_data = None

    print("\nWelcome to Course Project of Data Base by Ionov Serg\n")

    hh_api = HH_api()
    while True:
        print("Выберите ресурс по его номеру:\n")
        question = ('1 - Загрузить новые данные по работодателям и вакансиям\n'
                    '2 - Перейти к работе DBLoader\n'
                    '3 - Перейти к работе DBManager\n'
                    '4 - Выход из программы')
        count = 4
        answer = get_user_answer(question, count)

        if answer == 4:
            exit()

        # Операции сортировки / фильтрации / сравнения вакансий
        elif answer == 1:
            # Запуск цикла вопросов
            while True:
                print("Выберите ресурс по его номеру:\n")
                question = ('1 - Выбрать список работодателей\n'
                            '2 - Получить список работодателей по ключевому слову\n'
                            '3 - Выход в меню')
                count = 3
                answer = get_user_answer(question, count)

                # Выход из программы
                if answer == 3:
                    break

                elif answer == 1:

                    # Список компаний для парсинга
                    employers_list = [{'name': 'Boxberry', 'id': '80660'},
                                      {'name': 'IT-company Умная Логистика', 'id': '1708289'},
                                      {'name': 'Первый Бит', 'id': '3177'},
                                      {'name': 'IT-Компания АБС', 'id': '740349'},
                                      {'name': 'SberTech', 'id': '906557'},
                                      {'name': 'Softline', 'id': '2381'},
                                      {'name': 'ИК СИБИНТЕК', 'id': '197135'},
                                      {'name': 'IT-Сервис', 'id': '3735331'},
                                      {'name': 'Иннотех, Группа компаний', 'id': '4649269'},
                                      {'name': 'Labirint IT', 'id': '6082361'}]
                    employers_data = []
                    for employer in employers_list:
                        data = hh_api.get_company_info(employer['id'])
                        employers_data.append(data)
                    print(f'Получены данные о {len(employers_data)} работодателях')

                elif answer == 2:

                    keyword = input("Введите слово для поиска работодателя:\n").strip()
                    if not keyword:
                        keyword = "python"
                    employers_data = hh_api.get_employers(keyword=keyword)

        # работа DBLoader
        elif answer == 2:
            password = input('Для работы с БД postgreSQL введите пароль:\n')

            loader = DB_Loader(host, database, user, password)

            employers_list = get_employers_id(employers_data)
            vacancies_data = hh_api.get_vacancies(employers_list)
            vacancies_data = get_formatted_vacancy(vacancies_data)

            # Запуск цикла вопросов
            while True:
                print("Какие операции хотите произвести?\n")
                question = ('1 - Создать таблицы\n'
                            '2 - Очистить таблицы и заполнить новыми данными\n'
                            '3 - Выход в меню')
                count = 3
                answer = get_user_answer(question, count)

                # Выход из программы
                if answer == 3:
                    break

                elif answer == 1:

                    loader.create_employers()
                    loader.create_vacancies()

                elif answer == 2:
                    loader.delete_all()
                    loader.fill_employers(employers_data)
                    loader.fill_vacancies(vacancies_data)

        # работа DBManager
        elif answer == 3:
            password = input('Для работы с БД postgreSQL введите пароль:\n')

            db_manager = DB_Manager(host, database, user, password)
            # Запуск цикла вопросов
            while True:
                print('\nКакие операции c базой данных хотите произвести?\n')
                question = ('1 - Вывести список всех компаний и количество вакансий у каждой компании.\n'
                            '2 - Вывести список всех вакансий с указанием названия компании, названия вакансии,'
                            ' зарплаты и ссылки на вакансию.\n'
                            '3 - Вывести среднюю зарплату по всем вакансиям.\n'
                            '4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
                            '5 - Вывести список всех вакансий, в названии которых содержатся переданные в метод слова,'
                            ' например “python”.\n'
                            '6 - Выход в меню')

                count = 6
                answer = get_user_answer(question, count)
                data = None

                # Выход из программы
                if answer == 6:
                    break

                elif answer == 1:
                    data = db_manager.get_companies_and_vacancies_count()

                elif answer == 2:
                    data = db_manager.get_all_vacancies()

                elif answer == 3:
                    data = db_manager.get_avg_salary()

                elif answer == 4:
                    data = db_manager.get_vacancies_with_higher_salary()

                elif answer == 5:
                    keyword = input("Введите слово для поиска вакансии:\n").strip()
                    data = db_manager.get_vacancies_with_keyword(keyword)

                print(data, sep='\n')