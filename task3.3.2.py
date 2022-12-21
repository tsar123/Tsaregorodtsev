import math
import pandas as pd

class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        #vacancies_dif_currencies.csv

    @staticmethod
    def prepare():
        fr = pd.read_csv(input("Введите название файла: "))
        currencyFile = "dataframe.csv"
        df = pd.read_csv(currencyFile)
        return fr, df

class CurrencyFrame:
    @staticmethod
    def currencyToRub(fr, df):
        fr.insert(1, "salary", None)
        fr["salary"] = fr[["salary_from", "salary_to"]].mean(axis=1)
        fr["salary"] = fr["salary"].astype + " " + fr["salary_currency"] + " " + fr["published_at"]
        fr["salary"] = fr["salary"].apply(lambda x: CurrencyFrame.converter(x, df))
        CurrencyFrame.fileCropp(fr)

    @staticmethod
    def converter(x, df):
        if pd.isnull(x):
            return x
        values = x.split()
        if df.columns.__contains__(values[1]):
            d = values[2]
            currency = df[df["date"] == d[:7]][values[1]].values
            if not math.isnan(currency[0]):
                return round(float(values[0]) * currency[0])
        return x

    @staticmethod
    def fileCropp(x):
        x = x.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
        (x.head(100)).to_csv("new_dataframe.csv", index=False)


input = InputConnect()
CurrencyFrame.currencyToRub(input.params[0], input.params[1])
