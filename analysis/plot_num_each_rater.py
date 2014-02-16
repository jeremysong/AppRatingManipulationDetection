__author__ = 'jeremy'

import MySQLdb
from datetime import datetime
import matplotlib.pyplot as plt
import numpy


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
            comment_dict[week_key] = [rating]
        else:
            comment_dict[week_key].append(rating)

    cur.close()
    db.close()

    rating_order_by_week = [comment_dict[index] for index in sorted(comment_dict.iterkeys())]

    print(comment_dict)
    print(rating_order_by_week)

    oneStarRatings = list()
    twoStarRatings = list()
    threeStarRatings = list()
    fourStarRatings = list()
    fiveStarRatings = list()

    for ratings in rating_order_by_week:
        oneStarRatings.append(ratings.count(1))
        twoStarRatings.append(ratings.count(2))
        threeStarRatings.append(ratings.count(3))
        fourStarRatings.append(ratings.count(4))
        fiveStarRatings.append(ratings.count(5))

    print(oneStarRatings)

    ax = plt.subplot()
    ax.set_ylabel('Number of ratings')
    ax.set_xlabel('Week')
    bar1 = ax.bar(numpy.arange(1, len(comment_dict) + 1) - 0.3, oneStarRatings, color='r', width=0.15)
    bar2 = ax.bar(numpy.arange(1, len(comment_dict) + 1) - 0.15, twoStarRatings, color='g', width=0.15)
    bar3 = ax.bar(numpy.arange(1, len(comment_dict) + 1), threeStarRatings, color='b', width=0.15)
    bar4 = ax.bar(numpy.arange(1, len(comment_dict) + 1) + 0.15, fourStarRatings, color='grey', width=0.15)
    bar5 = ax.bar(numpy.arange(1, len(comment_dict) + 1) + 0.3, fiveStarRatings, color='brown', width=0.15)
    ax.legend([bar1, bar2, bar3, bar4, bar5], ['1 star', '2 star', '3 star', '4 star', '5 star'])
    plt.show()


if __name__ == '__main__':
    __app_id = '565200595'
    __app_version = '2.0'
    __db_name = 'Crawler_apple_us'
    plot(__app_id, db_name=__db_name, version=False)