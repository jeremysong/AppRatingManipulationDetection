from collections import defaultdict
from datetime import datetime
import MySQLdb
import numpy
import matplotlib.pyplot as plt
from data_processor.datePatterns import DatePatterns

__author__ = 'jeremy'


def plot(app_id, app_version=None, db_name='Crawler_apple', date_format=DatePatterns.itunes_date_pattern, version=True):
    db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT rating, date FROM Comment WHERE app_id=" + "'" + app_id + "'"
    if version:
        comment_sql = comment_sql + " and device_version='" + app_version + "'"
    #comment_sql = "SELECT rating, date FROM Comment WHERE app_id=" + "'" + app_id + "'"
    cur.execute(comment_sql)

    comment_dict = defaultdict(int)

    for comment_row in cur.fetchall():
        date = datetime.strptime(str(comment_row[1]).split(' ')[0], date_format).date()
        isoCalendar = date.isocalendar()
        year = isoCalendar[0]
        nth_week = isoCalendar[1]
        week_key = str(year) + '.' + str(nth_week) if nth_week >= 10 else str(year) + '.0' + str(nth_week)
        comment_dict[week_key] += 1

    cur.close()
    db.close()

    rating_order_by_week = [comment_dict[index] for index in sorted(comment_dict.iterkeys())]
    max_num = max(rating_order_by_week)
    min_num = min(rating_order_by_week)
    threshold = 0.7 * (max_num - min_num) + min_num

    print('Max num rating: {0}. Threshold: {1}.'.format(max_num, threshold))

    ax = plt.subplot()
    ax.set_ylabel('Number of Reviews')
    ax.set_xlabel('Week')
    ax.bar(numpy.arange(1, len(rating_order_by_week)+1, 1), rating_order_by_week, edgecolor='b', width=1.0)
    plt.xlim([1, len(rating_order_by_week)])
    plt.xticks(numpy.arange(1, len(rating_order_by_week) + 1, 10))
    plt.ylim([1, max(rating_order_by_week)])
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    __app_id = 'B006PHD0RW'
    __app_version = '2.0'
    __db_name = 'Crawler_amazon_us'
    plot(__app_id, db_name=__db_name, date_format=DatePatterns.amazon_date_pattern , version=False)