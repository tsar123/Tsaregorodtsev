import sqlite3 as al
import pandas as pd


class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        #database_test.db
        #vacancies_dif_currencies.csv

    @staticmethod
    def prepare():
        db = input("Введите название базы данных: ")
        fr = pd.read_csv(input("Введите название файла: "))

        return db, fr


class TransferToDatabase:
    @staticmethod
    def convertToRu(x, cur):
        if pd.isnull(x):
            return x
        string = x.split()
        if string[1] in ["RUR", "AZN", "UZS", "KGS", "GEL"]:
            return string[0]

        cur.execute(f"""
        SELECT date, {string[1]} FROM CurrencyFrame
        WHERE date = '{string[2]}'
        """)
        val = cur.fetchone()
        if val != None:
            print(val)
        if val[1] is not None:
            return round(float(string[0]) * val[1])
        return string[0]

    @staticmethod
    def createTable(db, fr):
        sqlite3Сonnection = al.connect(db)
        cur = sqlite3Сonnection.cursor()

        fr.insert(1, "salary", None)
        fr["salary"] = fr[["salary_from", "salary_to"]].mean(axis=1)
        fr["published_at"] = fr["published_at"].apply(lambda d: d[:7])
        fr["salary"] = fr["salary"].astype(str) + " " + + fr["salary_currency"] + " " + fr["published_at"]
        fr["salary"] = fr["salary"].apply(lambda x: TransferToDatabase.convertToRu(x, cur))
        fr = fr.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

        fr.to_sql('Vacancy', sqlite3Сonnection, if_exists='replace', index=False)
        cur.close()
        if (sqlite3Сonnection == True):
            sqlite3Сonnection.close()


input = InputConnect()
TransferToDatabase.createTable(input.params[0], input.params[1])
