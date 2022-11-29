import csv
from _datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

currencyToRub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}


class Vacancy:
    """Класс Vacancy устанавливает все основные поля вакансии

        Attributes:
            name (str): название файла,
            salary (int): зарплата,
            area_name (str): город,
            published_at (str): дата и время публикации
        """
    def __init__(self, name, salary, area_name, published_at):
        """Инициализирует объект Vacancy

        Args:
            name (str): название файла,
            salary (int): зарплата,
            area_name (str): город,
            published_at (str): дата и время публикации
        """
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    """Класс для предоставления зарплаты

    Attributes:
        salary_from (int): нижняя граница вилки оклада,
        salary_to (int): верхняя граница вилки оклада,
        salary_currency (str): валюта оклада
    """
    def __init__(self, salary_from, salary_to, salary_currency):
        """Инициализирует объект Salary и выполняет конвертацию для целых полей

        Args:
            salary_from (str или int или float): нижняя граница вилки оклада,
            salary_to (str или int или float): верхняя граница вилки оклада,
            salary_currency (str или int или float): валюта оклада
            salary_ru (float): средняя зарплата из вилки в рублях, переводит при помощи словаря - currencyToRub
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.salary_ru = int((float(self.salary_from) + float(self.salary_to)) / 2) * currencyToRub[
            self.salary_currency]

    def get_salary_ru(self):
        """Возвращает вычисление salary_ru

        Returns:
            float: средняя зарплата в рублях
        """
        return self.salary_ru


class DataSet:
    """Класс DataSet отвечает за чтение и подготовку данных

    Attributes:
        file_name (str): название файла
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet

        Args:
            file_name (str или int или float): название файла
            vacancies_objects (str или int или float): название профессии
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.prepare(file_name)

    @staticmethod
    def csv_reader(filename):
        """Осуществляет выход, если файл пустой или возвращает колонки и строки

        Returns:
            tuple: колонки, строки
        """
        with open(filename, encoding="utf-8-sig") as f:
            data = [x for x in csv.reader(f)]
        try:
            clmns = data[0]
            lines = data[1:]
            return clmns, lines
        except FileNotFoundError:
            print("Пустой файл")
            exit()

    @staticmethod
    def prepare(filename):
        """Возвращает список с данными по одной вакансии

        Returns:
            list: список с данными по одной вакансии
        """
        clmns, lines = DataSet.csv_reader(filename)
        filtred = [i for i in lines if len(i) == len(clmns) and '' not in i]
        vac = []
        for line in filtred:
            dct = {}
            for x in range(0, len(line)):
                if line[x].count('\n') > 0:
                    read = [DataSet.remove_tags(el) for el in line[x].split('\n')]
                else:
                    read = DataSet.remove_tags(line[x])
                dct[clmns[x]] = read

            vac.append(Vacancy(dct['name'], Salary(dct['salary_from'],
                                                   dct['salary_to'], dct['salary_currency']), dct['area_name'],
                               dct['published_at']))
        return vac

    @staticmethod
    def remove_tags(args):
        """Возвращает вводимые данные без тегов

        Returns:
            str: вводимые данные без тегов
        """
        return " ".join(re.sub(r"\<[^>]*\>", "", args).split())


class InputConnect:
    """Класс InputConect отвечает за обработку параметров вводимых пользователем и

    Attributes:

    """
    def __init__(self):
        """Инициализирует объект InputConnect

        Args:

        """
        self.params = InputConnect.get_prms()

    @staticmethod
    def get_prms():
        """Возвращает вводимые название файла и название профессии

        Returns:
            tuple: название файла, название профессии
        """
        file_name = input("Введите имя файла: ")
        vacancy = input("Введите название профессии")
        return file_name, vacancy

    @staticmethod
    def first_corr(dic):
        """Возвращает словарь из дессяти первых значений

        Returns:
            dict: десять первых значений
        """
        res = {}
        i = 0
        for key, value in dic.items():
            res[key] = value
            i += 1
            if i == 10:
                break
        return res

    @staticmethod
    def print(dic_vacancies, vac_name):
        """Возвращает значения для построения диграмм

        Returns:
            dict: динамика зарплат, уровня зарплат, количества вакансий по годам
            float: уровень зарплат по городам, доля вакансий по городам
        """
        years = set()
        for vacancy in dic_vacancies:
            years.add(int(datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y')))
        years = sorted(list(years))
        years = list(range(min(years), max(years) + 1))
        salary_years = {year: [] for year in years}
        vacs_years = {year: 0 for year in years}
        vac_salary_years = {year: [] for year in years}
        vac_count_years = {year: 0 for year in years}
        for vacancy in dic_vacancies:
            year = int(datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y'))
            salary_years[year].append(vacancy.salary.get_salary_ru())
            vacs_years[year] += 1
            if vac_name in vacancy.name:
                vac_salary_years[year].append(vacancy.salary.get_salary_ru())
                vac_count_years[year] += 1

        salary_years = {key: int(sum(value) / len(value)) if len(value) != 0 else 0
                        for key, value in salary_years.items()}
        vac_salary_years = {key: int(sum(value) / len(value)) if len(value) != 0 else 0
                            for key, value in vac_salary_years.items()}
        area_dic = {}
        for vacancy in dic_vacancies:
            if vacancy.area_name in area_dic:
                area_dic[vacancy.area_name].append(vacancy.salary.get_salary_ru())
            else:
                area_dic[vacancy.area_name] = [vacancy.salary.get_salary_ru()]

        area_salary = [x for x in area_dic.items() if len(x[1]) / len(dic_vacancies) > 0.01]
        sort_area_salary = sorted(area_salary, key=lambda item: sum(item[1]) / len(item[1]), reverse=True)
        res_sort_area_salary = {item[0]: int(sum(item[1]) / len(item[1])) for item in sort_area_salary}
        fract_vac_area = {
            key: round(len(value) / len(dic_vacancies), 4) if len(value) / len(dic_vacancies) > 0.01 else 0
            for key, value in area_dic.items()}
        fract_vac_area = {key: value for key, value in fract_vac_area.items() if value != 0}
        sort_fract_vac_area = sorted(fract_vac_area.items(), key=lambda item: item[1], reverse=True)
        res_sort_fract_vac_area = {k: v for k, v in sort_fract_vac_area}
        print('Динамика уровня зарплат по годам: {}'.format(salary_years))
        print('Динамика количества вакансий по годам: {}'.format(vacs_years))
        print('Динамика уровня зарплат по годам для выбранной профессии: {}'.format(vac_salary_years))
        print('Динамика количества вакансий по годам для выбранной профессии: {}'.format(vac_count_years))
        print('Уровень зарплат по городам (в порядке убывания): {}'.format(InputConnect.first_corr(res_sort_area_salary)))
        print('Доля вакансий по городам (в порядке убывания): {}'.format(InputConnect.first_corr(res_sort_fract_vac_area)))
        return salary_years, vac_salary_years, vacs_years, vac_count_years, InputConnect.first_corr(res_sort_area_salary), InputConnect.first_corr(res_sort_fract_vac_area)


class Report:
    """Класс Report отвечает за формирование диграмм

    Attributes:

    """
    @staticmethod
    def replaceN(w):
        """Удаляет перенос строки и возвращает входящие исправленные данные

        Returns:
            dict: входящие данные без переноса
        """
        for k in list(w.keys()):
            if '-' in k:
                n = k.replace('-', '\n')
                w[n] = w[k]
                del w[k]
            if ' ' in k:
                n = k.replace(' ', '\n')
                w[n] = w[k]
                del w[k]

        w = {k: v for k, v in sorted(w.items(), key=lambda item: item[1], reverse=True)}
        return w

    @staticmethod
    def summaryOther(w):
        """Рассчитывает долю других городов не входящих в ТОП-10 городов и возвращает словарь

        Returns:
            dict: доля других городов не входящих в ТОП-10
        """
        w['Другие'] = 1 - sum(w.values())
        w = {k: v for k, v in sorted(w.items(), key=lambda item: item[1], reverse=True)}
        return w

    @staticmethod
    def makeDiagrams(info, vac):
        """Осуществляет компоновку и построение диграмм

        Returns:
            None
        """
        salary_years = info[0]
        vac_salary_years = info[1]
        vacs_years = info[2]
        vac_count_years = info[3]
        res_sort_area_salary = info[4]
        res_sort_fract_vac_area = info[5]
        width = 0.3
        x_nums = np.arange(len(salary_years.keys()))
        x_list1 = x_nums - width / 2
        x_list2 = x_nums + width / 2
        fig = plt.figure()
        ax = fig.add_subplot(221)
        ax.set_title('Уровень зарплат по годам')
        ax.bar(x_list1, salary_years.values(), width, label='средняя з/п')
        ax.bar(x_list2, vac_salary_years.values(), width, label=f'з/п {vac}')
        ax.set_xticks(x_nums, salary_years.keys(), rotation='vertical')
        ax.legend(fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        ax.grid(True, axis='y')
        ax = fig.add_subplot(222)
        ax.set_title('Количество вакансий по годам')
        ax.bar(x_list1, vacs_years.values(), width, label='количество вакансий')
        ax.bar(x_list2, vac_count_years.values(), width, label=f'Количество вакансий\n{vac}')
        ax.set_xticks(x_nums, salary_years.keys(), rotation='vertical')
        ax.legend(fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        ax.grid(True, axis='y')
        width_y = 0.6
        y_nums = np.arange(len(res_sort_area_salary.keys()))
        y_list1 = y_nums
        ax = fig.add_subplot(223)
        ax.set_title('Уровень зарплат по городам')
        ax.barh(y_list1, Report.replaceN(res_sort_area_salary).values(), width_y, )
        ax.set_yticks(y_nums, Report.replaceN(res_sort_area_salary).keys())
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=6)
        ax.grid(True, axis='x')
        plt.gca().invert_yaxis()
        ax = fig.add_subplot(224)
        ax.set_title('Доля вакансий по городам')
        ax.pie(Report.summaryOther(res_sort_fract_vac_area).values(), labels=Report.summaryOther(res_sort_fract_vac_area).keys(), textprops={'fontsize': 6})
        plt.tight_layout()
        plt.savefig('graphLAST.png')
        plt.show()

input = InputConnect()
data = DataSet.prepare(input.params[0])
info = InputConnect.print(data, input.params[1])
Report.makeDiagrams(info, input.params[1])
