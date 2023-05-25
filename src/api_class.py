import abc
import requests      # Для запросов по API
import json          # Для обработки полученных результатов
import time          # Для задержки между запросами


class All_api(abc.ABC):
    """Абстрактный класс для классов HH и SJ"""
    @abc.abstractmethod
    def get_employers(self, *args, **qwargs):
        pass


class HH_api(All_api):
    """Класс для получения данных по API с сайта HH.ru """

    @classmethod
    def get_employers(cls, keyword, region_id=113, c_page=10, count=100) -> json:
        """
        Получает данные через URL и возвращает в переменную для дальнейшей работы.
        :param keyword: ключевое слово (название профессии)
        :param region_id: id региона (города или области) 113-Россия
        :param c_page: кол-во страниц
        :param count: количество вакансий на странице (100 вакансий)
        :return: список вакансий, в формате json
        """
        url = "https://api.hh.ru/employers"

        params = {"text": keyword,
                  "area": region_id,
                  "type": "company",
                  "only_with_vacancies": True,
                  "per_page": count,
                  }

        all_employers = []

        for page in range(0, c_page + 1):
            params['page'] = page

            response = requests.get(url=url, params=params)

            if response.ok:
                employers = response.json()["items"]
                all_employers.extend(employers)
            else:
                time.sleep(0.2)
                print("Error:", response.status_code)
                print(f'Ошибка при выполнении запроса на странице {page}')

        print(f"По Вашему запросу найдено {len(all_employers)} работодателей на сайте headhunter.ru")

        return all_employers

    @classmethod
    def get_vacancies(cls, employer_id, region_id=113, c_page=1, count=100) -> json:
        """
        Получает данные через URL и возвращает в переменную для дальнейшей работы.
        :param keyword: ключевое слово (название профессии)
        :param employer_id: список id работодателей
        :param region_id: id региона (города или области) 113-Россия
        :param c_page: кол-во страниц
        :param count: количество вакансий на странице (100 вакансий)
        :return: список вакансий, в формате json
        """
        url = "https://api.hh.ru/vacancies"

        params = {"area": region_id,
                  #"text": keyword,
                  "page": 0,
                  "per_page": count,
                  "employer_id": employer_id,
                  "currency": "RUR"
                  }

        all_vacancies = []

        #for page in range(1, c_page + 1):
        #    params['page'] = page
        for id in employer_id:
            params['employer_id'] = id
            response = requests.get(url=url, params=params)

            if response.ok:
                vacancies = response.json()["items"]
                all_vacancies.extend(vacancies)
            else:
                time.sleep(0.2)
                print("Error:", response.status_code)
                print(f'Ошибка при выполнении запроса на странице {page}')

        print(f"По Вашему запросу найдено {len(all_vacancies)} вакансий на сайте headhunter.ru")

        return all_vacancies

    def get_company_info(self, employers_id):
        response = requests.get(f'https://api.hh.ru/employers/{employers_id}')
        data = {}
        if response.status_code == 200:
            item = response.content.decode()
            response.close()
            jsObj = json.loads(item)
            data['id'] = jsObj['id']
            data['name'] = jsObj['name']
            data['alternate_url'] = jsObj['alternate_url']
            data['open_vacancies'] = jsObj['open_vacancies']

        return data
