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


def residuals(l, y, x):
    """
    Residuals for estimating error
    """
    err = y - poisson(l).pmf(x)
    return err


def get_fitting_parameters(app_id, plot=False):
    """
    Find all the parameter lambda in Poisson distribution that fit the num of comment by week.
    Return a set of those parameters and number of total weeks
    """
    db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
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
    perc_comment = map(lambda m: m / float(total_comment), num_comment)
    x_range = np.arange(0, num_week, 1)

    l_set = set()
    max_index = [num_comment.index(m) for m in sorted(num_comment)[-int(math.ceil(len(num_comment) / 5.0)):]]

    for l0 in set(max_index):
        l_fit = optimize.leastsq(residuals, l0, args=(num_comment, x_range))
        if math.isnan(l_fit[0][0]):
            continue
        l_set.add(round(l_fit[0][0], 0))

    if plot:
        for l in l_set:
            poisson_y = poisson(l).pmf(x_range)
            plt.plot(x_range, poisson_y, color='r')
            plt.bar(x_range, perc_comment)
            plt.show()

    return l_set, num_week


if __name__ == '__main__':
    app_ids = ['515212842', '499814295', '517445720', '525378313', '485252012', '604354955', '492464375',
               '474429394', '460351323', '439212087', '525948761', '407413403', '592996284', '530854685',
               '570591217']

    for app_id in app_ids:
        fitting_params, weeks = get_fitting_parameters(app_id, plot=True)
        print(fitting_params, weeks)