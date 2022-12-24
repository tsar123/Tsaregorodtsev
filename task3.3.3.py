import pandas as pd
import requests as requests
from pandas import json_normalize
pd.set_option("expand_frame_repr", False)

date = {'date_from': "2022-12-20T21:00:00", 'date_to': "2022-12-22T00:00:00"}
urls = []
for i in range(0, 20):
    urls.append(f"https://api.hh.ru/vacancies?specialization=1&per_page=100&page={i}&date_from={date['date_from']}&date_to={date['date_to']}")

vacancies = []
for url in urls:
    res = requests.get(url).json()
    vacancies.extend(res["items"])

rf = json_normalize(vacancies)
fr = rf[["name", "salary.from", "salary.to", "salary.currency", "area.name", "published_at"]]
fr.columns = fr.columns.str.replace(".", "_")
fr.to_csv("new_vacancies.csv", index=False)
