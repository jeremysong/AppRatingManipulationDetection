"""
Fitting number of comments of each week to Gaussian distribution.
"""

__author__ = 'jeremy'

import math
import MySQLdb
from datetime import datetime
import numpy as np
from scipy.stats import norm
from scipy import optimize
import matplotlib.pyplot as plt


def residuals(params, y, x):
    """
    Residuals for estimating error
    """
    err = y - norm.pdf(x, params[0], params[1])
    return err


def get_fitting_parameters(app_id, plot=False):
    """
    Find all the parameter lambda in Gaussian distribution that fit the number of comment by week.
    Return a set of those parameters(in dictionary) and number of total weeks.
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
    max_index = [num_comment.index(m) for m in sorted(num_comment)[-int(math.ceil(len(num_comment) / 10.0)):]]
    # Only fits limited data instead of whole data set
    data_span = 0 if num_week <= 10 else 5

    for center in set(max_index):
        #l_fit = optimize.leastsq(residuals, [l0, 10], args=(num_comment, x_range))
        #l_set.add(str(round(l_fit[0][0], 0)) + ',' + str(l_fit[1]))
        upper_bound = num_week + 1 if center + data_span + 1 > num_week else center + data_span + 1
        lower_bound = 0 if center - data_span < 0 else center - data_span
        fitted_data = num_comment if num_week <= 10 else num_comment[lower_bound: upper_bound]
        print(fitted_data)
        mu, std = norm.fit(fitted_data)
        if math.isnan(mu):
            continue
        l_set.add(str(round(mu, 0)) + ',' + str(std))

    if plot:
        fig = plt.subplot()
        for l in l_set:
            params = map(float, l.split(','))
            gaussian_dist = norm.pdf(np.arange(0, num_week, 0.2), params[0], params[1])
            fig.plot(np.arange(0, num_week, 0.2), gaussian_dist)
        fig.plot(np.arange(0, num_week), perc_comment)
        #fig.legend()
        plt.show()

    return l_set, num_week


if __name__ == '__main__':
    app_ids = ['405229260']

    for app_id in app_ids:
        fitting_params, weeks = get_fitting_parameters(app_id, plot=True)
        print(fitting_params, weeks)