import sqlite3 as al
import pandas as pd


class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        # database_test.db
        # Аналитик

    @staticmethod
    def prepare():
        db = input("Введите название базы данных: ")
        fr = input("Введите название профессии: ")
        return db, fr


class TransferToDatabase:
    @staticmethod
    def createStatistic(db, fr):
        sqlite3Сonnection = al.connect(db)
        cur = sqlite3Сonnection.cursor()

        salaryEveryYear = ("""
        SELECT SUBSTRING(published_at, 1, 4) AS 'Год', ROUND(AVG(salary), 2) AS 'Средняя зарплата' FROM Vacancy
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        vacancyCount = ("""
        SELECT SUBSTRING(published_at, 1, 4) AS 'Год', COUNT(salary) AS 'Количество вакансий' FROM Vacancy
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        salaryCity = ("""
        SELECT area_name AS 'Город', ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам' FROM Vacancy
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM Vacancy) / 100
        ORDER BY ROUND(AVG(salary), 2) DESC 
        LIMIT 10
        """)

        vacancyCountCity = ("""
        SELECT area_name AS 'Город', 
        100 * COUNT(*) / (select COUNT(*) from Vacancy) AS 'Доля вакансий по городам' FROM Vacancy
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM Vacancy) / 100
        ORDER BY COUNT(*) DESC 
        LIMIT 10
        """)

        list = [salaryEveryYear, vacancyCount, salaryCity, vacancyCountCity]
        for i in range(0, len(list)):
            stat = pd.read_sql(list[i], sqlite3Сonnection)
            print(stat)
        cur.close()


input = InputConnect()
TransferToDatabase.createStatistic(input.params[0], input.params[1])
