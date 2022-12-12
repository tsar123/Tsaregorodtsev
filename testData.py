from pstats import Stats, SortKey
import cProfile
import task2
from datetime import datetime


#def format_date(date):
     #1 замер
     #return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y')
     #2 замер
     #return date[:4]
     #3 замер
     #date.split('-')
     #return date[0]

#cProfile.run('format_date("2022-12-08T22:24:09+0300")', 'restats')
cProfile.run('task2', 'restats')
p = Stats('restats')
p.sort_stats(SortKey.TIME).print_stats(5)