import pandas as pd
from  _datetime import datetime
from xml.etree import ElementTree
import numpy as np
import grequests


class InputConnect:
    def __init__(self):
        self.params = InputConnect.prepare()
        #vacancies_dif_currencies.csv

    @staticmethod
    def prepare():
        fr = pd.read_csv(input("Введите название файла: "))
        print(fr["salary_currency"].value_counts())
        fr["count"] = fr.groupby("salary_currency")["salary_currency"].transform("count")
        fr = fr[(fr["count"] > 5000)] #конвертировать валюты, которые встречаются > 5000 вакансий
        fr["published_at"] = fr["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), 1))
        title = fr["salary_currency"].unique()
        dateMin = fr["published_at"].min()
        dateMax = fr["published_at"].max()
        title = np.delete(title, 1)
        data = {item: [] for item in np.insert(title, 0, "date")}
        dates = pd.date_range(dateMin.strftime("%Y-%m"), dateMax.strftime("%Y-%m"), freq="MS")
        return title, data, dates

class CurrencyFrame:
    def __init__(self, fileName):
        self.fileName = fileName

    @staticmethod
    def collectExchangeRates(datesList, dataframe):
        site_CBR = []
        for d in datesList:
            t = pd.to_datetime(str(d))
            date = t.strftime('%d/%m/%Y')
            dataframe["date"].append(t.strftime('%Y-%m'))
            site_CBR.append(rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")

        return site_CBR

    @staticmethod
    def makeDataFrame(title, dataframe, datesList):
        site = CurrencyFrame.collectExchangeRates(datesList, dataframe)
        response = (grequests.get(url) for url in site)
        for res in grequests.map(response):
            data = {}
            root = ElementTree.fromstring((res).content)
            for el in root.iter('Valute'):
                args = []
                for n in el:
                    args.append(n.text)
                if title.__contains__(args[1]):
                    data[args[1]] = round(float(args[4].replace(',', '.')) / int(args[2]), 6)
            for key in title:
                if data.__contains__(key):
                    dataframe[key].append(data[key])
                else:
                    dataframe[key].append(None)
        fr = pd.DataFrame(dataframe)
        fr.to_csv("dataframe.csv", index=False)


input = InputConnect()
CurrencyFrame.makeDataFrame(input.params[0], input.params[1], input.params[2])