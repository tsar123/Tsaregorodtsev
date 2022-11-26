import csv
from _datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

currencyToRub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}


class Vacancy:
    def __init__(self, name, salary, area_name, published_at):
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.salary_ru = int((float(self.salary_from) + float(self.salary_to)) / 2) * currencyToRub[
            self.salary_currency]

    def get_salary_ru(self):
        return self.salary_ru


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.prepare(file_name)

    @staticmethod
    def csv_reader(filename):
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
        return " ".join(re.sub(r"\<[^>]*\>", "", args).split())


class InputConnect:
    def __init__(self):
        self.params = InputConnect.get_prms()

    @staticmethod
    def get_prms():
        file_name = input("Введите имя файла: ")
        vacancy = input("Введите название профессии")
        return file_name, vacancy

    @staticmethod
    def first_corr(dic):
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
    @staticmethod
    def replaceN(w):
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
        w['Другие'] = 1 - sum(w.values())
        w = {k: v for k, v in sorted(w.items(), key=lambda item: item[1], reverse=True)}
        return w

    @staticmethod
    def makeDiagrams(info, vac):
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
