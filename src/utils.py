def get_formatted_vacancy(data) -> list:
    """Принимает данные и форматирует"""
    all_vacancies = []

    for row in data:
        if row['salary']:
            salary_min = row['salary']['from'] if row['salary']['from'] else row['salary']['to']
            salary_max = row['salary']['to'] if row['salary']['to'] else salary_min
            currency = row["salary"]["currency"] if row["salary"]["currency"] else None
        else:
            salary_min = None
            salary_max = None
            currency = None

        requirement = row['snippet']['requirement'] if row['snippet']['requirement'] \
            else 'Нет требований'
        responsibility = row['snippet']['responsibility'] if row['snippet']['responsibility'] \
            else 'Нет описания'

        new_dict = {'id': row['id'], 'name': row['name'], 'alternate_url': row['alternate_url'],
                    'salary_min': salary_min, 'salary_max': salary_max, 'currency': currency,
                    'employer_id': row['employer']['id'],
                    'requirement': requirement, 'responsibility': responsibility}
        all_vacancies.append(new_dict)

    return all_vacancies


def get_user_answer(question, count):
    """
    Функция получения от пользователя целого числа, не более значения count.
    :param question: Вопрос для пользователя.
    :param count: Число ограниечение.
    :return: Целое число.
    """
    print(question)
    while True:
        n = input()
        if n.isdigit():
            n = int(n)
            if 0 < n < count + 1:
                return n
            else:
                print(f"Ошибка! Введенное число должно быть от 1 до {count}. Повторите ввод.")
        else:
            print("Ошибка! Введенное значение не является числом. Повторите ввод.")


def get_employers_id(data: list):
    """
    Функция получения списка id работодателей из словарей.
    :param data: Список словарей.
    :return: Список id работодателей.
    """
    list_id = []
    for x in data:
        list_id.append(x['id'])
    return list_id
