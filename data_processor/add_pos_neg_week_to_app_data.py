"""
Positive week: all the ratings happened in that week are 4 or 5 stars.
"""

__author__ = 'jeremy'

import csv
import MySQLdb
from datetime import datetime
import collections

appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/extrPosNegAppData.csv", 'r')
posNegWeekAppDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/posNegWeekAppData.csv", 'w')

appDataCsv = csv.reader(appDataFile, delimiter=',')
posNegWeekAppDataCsv = csv.writer(posNegWeekAppDataFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple_us")
cur = db.cursor()
comment_sql = "SELECT app_id, date, rating FROM Comment"
cur.execute(comment_sql)

# Key: app ID; Value: dictionary, whose key: yyyy.nth_week; value: list of ratings
comment_by_week_dict = dict()

for comment_row in cur.fetchall():
    app_id = comment_row[0]
    date = datetime.strptime(comment_row[1].split(" ")[0], '%m/%d/%y').date()
    rating = comment_row[2]
    isoCalendar = date.isocalendar()
    # Use ISO calendar year here. For example, for 2012-01-01, it will return 2011, 52, 7
    year = isoCalendar[0]
    nth_week = isoCalendar[1]
    week_key = str(year) + str(nth_week) if nth_week >= 10 else str(year) + '0' + str(nth_week)
    if app_id not in comment_by_week_dict:
        comment_by_week_dict[app_id] = {week_key: [rating]}
    else:
        if week_key not in comment_by_week_dict[app_id]:
            comment_by_week_dict[app_id][week_key] = [rating]
        else:
            comment_by_week_dict[app_id][week_key].append(rating)

appDataFileHeader = next(appDataCsv)
appDataFileHeader.extend(['num_pos_week', 'perc_pos_week', 'num_neg_week', 'perc_neg_week', 'max_pos_week',
                          'perc_max_pos_week', 'max_neg_week', 'perc_max_neg_week'])

posNegWeekAppDataCsv.writerow(appDataFileHeader)


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


for app_data_row in appDataCsv:
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

    posNegWeekAppDataCsv.writerow(app_data_row)

appDataFile.close()
posNegWeekAppDataFile.close()




