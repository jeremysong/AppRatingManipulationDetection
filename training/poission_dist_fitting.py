"""
Fitting number of comments of each week to poisson distribution
"""
import math

__author__ = 'jeremy'

import MySQLdb
from datetime import datetime
import numpy as np
from scipy.stats import poisson
from scipy import optimize
import matplotlib.pylab as plt

#app_id = '515212842'
#app_id = '499814295'
#app_id = '525378313'
#app_id = '485252012'
#app_id = '604354955'
#app_id = '492464375'
#app_id = '474429394'
#app_id = '460351323'
#app_id = '439212087'
#app_id = '525948761'
#app_id = '485252012'
#app_id = '499814295'
#app_id = '592996284'
#app_id = '530854685'
app_id = '407413403'
#app_id = '517445720'
#app_id = '570591217'

db = db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT date, COUNT(*) FROM Comment WHERE app_id=" + "'" + app_id + "'" + "GROUP BY date "
cur.execute(comment_sql)

comment_by_week = dict()

for comment_row in cur.fetchall():
    date = datetime.strptime(comment_row[0].split(' ')[0], '%m/%d/%y').date()
    num_comment = int(comment_row[1])
    isoCalendar = date.isocalendar()
    year = isoCalendar[0]
    nth_week = isoCalendar[1]
    week_key = str(year) + str(nth_week) if nth_week >= 10 else str(year) + '0' + str(nth_week)
    if week_key not in comment_by_week:
        comment_by_week[week_key] = num_comment
    else:
        comment_by_week[week_key] += num_comment

num_comment = [comment_by_week[week_key] for week_key in sorted(comment_by_week.iterkeys())]
num_week = len(num_comment)
total_comment = sum(num_comment)
perc_comment = map(lambda m: m/float(total_comment), num_comment)
x_range = np.arange(0, num_week, 1)


def residules(l, y, x):
    err = y - poisson(l).pmf(x)
    return err

l_set = set()

max_index = [num_comment.index(m) for m in sorted(num_comment)[-len(num_comment)/5:]]
print(max_index)

max_index = max_index if np.nan not in max_index else max_index.remove(np.nan)

for l0 in set(max_index):
    l_fit = optimize.leastsq(residules, l0, args=(num_comment, x_range))
    l_set.add(round(l_fit[0][0], 0))

print(l_set)

for l in l_set:
    poisson_y = poisson(l).pmf(x_range)
    plt.plot(x_range, poisson_y, color='r')
plt.bar(x_range, perc_comment)
plt.show()

