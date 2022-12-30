import sqlite3 as al
import pandas as pd


class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        #test_database.db
        #dataframe.csv

    @staticmethod
    def prepare():
        db = input("Введите название базы данных: ")
        fr = pd.read_csv(input("Введите название файла: "))

        return db, fr


class TransferToDatabase:
    @staticmethod
    def createTable(db, fr):
        sqlite3Сonnection = al.connect(db)
        cur = sqlite3Сonnection.cursor()
        database = """
        CREATE TABLE CurrencyFrame(
                date text,
                BYR float,
                USD float,
                EUR float,
                KZT float,
                UAH float,
                AZN float,
                KGS float,
                UZS float
            ); 
            """
        cur.execute(database)
        sqlite3Сonnection.commit()
        fr.to_sql('CurrencyFrame', sqlite3Сonnection, if_exists='replace', index=False)
        cur.close()
        if (sqlite3Сonnection == True):
            sqlite3Сonnection.close()


input = InputConnect()
TransferToDatabase.createTable(input.params[0], input.params[1])
