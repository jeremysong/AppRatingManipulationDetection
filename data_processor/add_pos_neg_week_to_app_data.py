"""
Positive week: all the ratings happened in that week are 4 or 5 stars.
"""

__author__ = 'jeremy'

import csv
import MySQLdb
from datetime import datetime
import collections


def pos_week(ratings):
    if min(map(int, ratings)) <= 3:
        return 0
    else:
        return 1


def neg_week(ratings):
    if max(map(int, ratings)) >= 3:
        return 0
    else:
        return 1


def max_continuous_value(ratings, v):
    max_length = 0
    current = 0
    for value in ratings:
        if value == v:
            current += 1
        else:
            max_length = max([max_length, current])
            current = 0
    max_length = max([max_length, current])
    return max_length


def generate_features(data_path, host, user, passwd, db_name, date_pattern):
    app_data_file = open(data_path + "extrPosNegAppData.csv", 'r')
    pos_neg_week_app_data_file = open(data_path + "posNegWeekAppData.csv", 'w')

    app_data_csv = csv.reader(app_data_file, delimiter=',')
    pos_neg_week_app_data_csv = csv.writer(pos_neg_week_app_data_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT app_id, date, rating FROM Comment"
    cur.execute(comment_sql)

    # Key: app ID; Value: dictionary, whose key: yyyy.nth_week; value: list of ratings
    comment_by_week_dict = dict()

    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        date = datetime.strptime(str(comment_row[1]).split(" ")[0], date_pattern).date()
        rating = comment_row[2]
        iso_calendar = date.isocalendar()
        # Use ISO calendar year here. For example, for 2012-01-01, it will return 2011, 52, 7
        year = iso_calendar[0]
        nth_week = iso_calendar[1]
        week_key = str(year) + str(nth_week) if nth_week >= 10 else str(year) + '0' + str(nth_week)
        if app_id not in comment_by_week_dict:
            comment_by_week_dict[app_id] = {week_key: [rating]}
        else:
            if week_key not in comment_by_week_dict[app_id]:
                comment_by_week_dict[app_id][week_key] = [rating]
            else:
                comment_by_week_dict[app_id][week_key].append(rating)

    app_data_file_header = next(app_data_csv)
    app_data_file_header.extend(['num_pos_week', 'perc_pos_week', 'num_neg_week', 'perc_neg_week', 'max_pos_week',
                                 'perc_max_pos_week', 'max_neg_week', 'perc_max_neg_week'])

    pos_neg_week_app_data_csv.writerow(app_data_file_header)

    for app_data_row in app_data_csv:
        app_id = app_data_row[0]
        rating_week_dict = collections.OrderedDict(sorted(comment_by_week_dict[app_id].items()))
        pos_week_list = [pos_week(week_ratings) for week_ratings in rating_week_dict.itervalues()]
        neg_week_list = [neg_week(week_ratings) for week_ratings in rating_week_dict.itervalues()]
        total_week = float(len(rating_week_dict))
        num_pos_week = sum(pos_week_list)
        num_neg_week = sum(neg_week_list)
        perc_pos_week = num_pos_week / total_week
        perc_neg_week = num_neg_week / total_week
        max_pos_week = max_continuous_value(pos_week_list, 1)
        max_neg_week = max_continuous_value(neg_week_list, 1)
        perc_max_pos_week = max_pos_week / total_week
        perc_max_neg_week = max_neg_week / total_week

        app_data_row.extend([num_pos_week, perc_pos_week, num_neg_week, perc_neg_week, max_pos_week, perc_max_pos_week,
                             max_neg_week, perc_max_neg_week])

        pos_neg_week_app_data_csv.writerow(app_data_row)

    app_data_file.close()
    pos_neg_week_app_data_file.close()
    print('Finish adding positive and negative week features.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'
    __date_pattern = '%m/%d/%y'

    generate_features(__data_path, __host, __user, __passwd, __db_name, __date_pattern)





