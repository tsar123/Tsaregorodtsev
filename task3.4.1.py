import math
import pandas as pd


class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        #vacancies_dif_currencies.csv
        #dataframe.csv

    @staticmethod
    def prepare():
        fr = pd.read_csv(input("Введите название файла: "))
        df = pd.read_csv(input("Введите название второго файла: "))

        fr.insert(1, "salary", None)
        fr.assign(salary=lambda x: x.salary_from)
        fr["salary"] = fr[["salary_from", "salary_to"]].mean(axis=1)
        fr["salary"] = fr["salary"].astype(str) + " " + + fr["salary_currency"] + " " + fr["published_at"]
        fr["salary"] = fr["salary"].apply(lambda x: CurrencyFrame.converterToRub(x, df))

        CurrencyFrame.makeFrame(fr)

class CurrencyFrame:
    @staticmethod
    def converterToRub(f, df):
        if pd.isnull(f):
            return f
        values = f.split()
        if df.columns.__contains__(values[1]):
            d = values[2]
            course = df[df["date"] == d[:7]][values[1]].values
            if not math.isnan(course[0]):
                return round(float(values[0]) * course[0])
        return f

    @staticmethod
    def makeFrame(vac):
        vac = vac.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
        vacHundred = vac.head(100)
        vacHundred.to_csv("100head_dataframe.csv", index=False)

input = InputConnect()
#CurrencyFrame.makeFrame(input)
