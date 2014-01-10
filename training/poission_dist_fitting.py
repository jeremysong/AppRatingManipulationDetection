"""
Fitting number of comments of each week to poisson distribution
"""

__author__ = 'jeremy'

import MySQLdb
from datetime import datetime
import numpy as np
from scipy.stats import poisson
from scipy import optimize
import matplotlib.pylab as plt

#app_id = '515212842'
app_id = '499814295'
#app_id = '515212842'
#app_id = '485252012'
#app_id = '604354955'
#app_id = '492464375'

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
x = np.arange(0, num_week, 1)


def residules(l, y, x):
    err = y - poisson(l).pmf(x)
    return err

l0 = num_week/2
l_fit = optimize.leastsq(residules, l0, args=(num_comment, x))
print(l_fit[0])

poisson_y = poisson(l_fit[0]).pmf(x)

plt.plot(x, poisson_y, color='r')
plt.bar(x, perc_comment)
plt.show()