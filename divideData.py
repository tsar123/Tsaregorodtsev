import pandas as pd
from task2 import FormatDate

class DivideData:
    def __init__(self, fileName):
        pd.set_option('expand_frame_repr', False)
        df = pd.read_csv(fileName)
        df['years'] = df['published_at'].apply(FormatDate)
        years = df['years'].unique()
        for e in years:
            data = df[df['years'] == e]
            data.drop(columns='years').to_csv(rf'files_by_year\{e}_year.csv', index=False)

#DivideData('vacancies_big.csv')
DivideData('vacancies_by_year.csv')