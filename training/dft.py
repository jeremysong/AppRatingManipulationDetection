__author__ = 'jeremy'

import MySQLdb
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def plot(app_id, app_version=None, db_name='Crawler_apple_us', version=True):
    db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT rating, date FROM Comment WHERE app_id=" + "'" + app_id + "'"
    if version:
        comment_sql = comment_sql + " and device_version='" + app_version + "'"
    #comment_sql = "SELECT rating, date FROM Comment WHERE app_id=" + "'" + app_id + "'"
    cur.execute(comment_sql)

    comment_dict = dict()

    for comment_row in cur.fetchall():
        rating = int(comment_row[0])
        date = datetime.strptime(comment_row[1].split(' ')[0], '%m/%d/%y').date()
        isoCalendar = date.isocalendar()
        year = isoCalendar[0]
        nth_week = isoCalendar[1]
        week_key = str(year) + '.' + str(nth_week) if nth_week >= 10 else str(year) + '.0' + str(nth_week)
        if week_key not in comment_dict:
            comment_dict[week_key] = 1
        else:
            comment_dict[week_key] += 1

    cur.close()
    db.close()

    rating_order_by_week = [comment_dict[index] for index in sorted(comment_dict.iterkeys())]

    print(comment_dict)
    print(rating_order_by_week)

    freq = np.fft.fft(rating_order_by_week)
    plt.plot(range(1, len(rating_order_by_week) + 1, 1), freq)
    plt.plot(range(1, len(rating_order_by_week) + 1, 1), rating_order_by_week)
    plt.show()


if __name__ == '__main__':
    __app_id = '513274238'
    __app_version = '2.0'
    __db_name = 'Crawler_apple'
    plot(__app_id, db_name=__db_name, version=False)