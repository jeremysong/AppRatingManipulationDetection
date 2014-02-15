"""
Add correlation coefficient between number of positive ratings(4,5) and negative ratings(1,2) by week to app data
"""
import csv
from datetime import datetime
import MySQLdb
import numpy as np

__author__ = 'jeremy'


def generate_features(data_path, host, user, passwd, db_name, date_pattern):
    app_data_file = open(data_path + "varVersionRatingAppData.csv", 'r')
    coef_pos_neg_rating = open(data_path + "coefPosNegRatingsAppData.csv", 'w')
    app_data_file_csv = csv.reader(app_data_file, delimiter=',')
    coef_pos_neg_rating_csv = csv.writer(coef_pos_neg_rating, delimiter=',')

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
        week_key = str(year) + '.' + str(nth_week)
        if app_id not in comment_by_week_dict:
            comment_by_week_dict[app_id] = {week_key: [rating]}
        else:
            if week_key not in comment_by_week_dict[app_id]:
                comment_by_week_dict[app_id][week_key] = [rating]
            else:
                comment_by_week_dict[app_id][week_key].append(rating)

    # App data header
    app_data_file_header = next(app_data_file_csv)
    app_data_file_header.append("coef_pos_neg_rating_by_week")
    app_data_file_header.append("coef_1_5_num_rating")
    app_data_file_header.append("coef_2_5_rating_by_week")
    app_data_file_header.append("coef_3_5_rating_by_week")
    app_data_file_header.append("coef_avg_rating_num_by_week")

    coef_pos_neg_rating_csv.writerow(app_data_file_header)

    for app_data_row in app_data_file_csv:
        app_id = app_data_row[0]
        rating_week_dict = comment_by_week_dict[app_id]
        num_pos_rating_by_week = list()
        num_neg_rating_by_week = list()
        num_rating_by_week = list()
        avg_rating_by_week = list()
        num_1_rating_by_week = list()
        num_2_rating_by_week = list()
        num_3_rating_by_week = list()
        num_4_rating_by_week = list()
        num_5_rating_by_week = list()
        for week_key in rating_week_dict:
            num_rating = len(rating_week_dict[week_key])
            avg_rating = np.average(rating_week_dict[week_key])
            num_pos_rating = rating_week_dict[week_key].count(5) + rating_week_dict[week_key].count(4)
            num_neg_rating = rating_week_dict[week_key].count(1) + rating_week_dict[week_key].count(2)
            num_1_rating = rating_week_dict[week_key].count(1)
            num_2_rating = rating_week_dict[week_key].count(2)
            num_3_rating = rating_week_dict[week_key].count(3)
            num_4_rating = rating_week_dict[week_key].count(4)
            num_5_rating = rating_week_dict[week_key].count(5)
            num_rating_by_week.append(num_rating)
            avg_rating_by_week.append(avg_rating)
            num_pos_rating_by_week.append(num_pos_rating)
            num_neg_rating_by_week.append(num_neg_rating)
            num_1_rating_by_week.append(num_1_rating)
            num_2_rating_by_week.append(num_2_rating)
            num_3_rating_by_week.append(num_3_rating)
            num_4_rating_by_week.append(num_4_rating)
            num_5_rating_by_week.append(num_5_rating)

        coef_pos_neg_num_rating = np.corrcoef(np.vstack((num_pos_rating_by_week, num_neg_rating_by_week)))[0][1]
        coef_1_5_num_rating = np.corrcoef(np.vstack((num_1_rating_by_week, num_5_rating_by_week)))[0][1]
        coef_2_5_num_rating = np.corrcoef(np.vstack((num_2_rating_by_week, num_5_rating_by_week)))[0][1]
        coef_3_5_num_rating = np.corrcoef(np.vstack((num_3_rating_by_week, num_5_rating_by_week)))[0][1]
        coef_avg_rating_num = np.corrcoef(np.vstack((num_rating_by_week, avg_rating_by_week)))[0][1]
        app_data_row.append(coef_pos_neg_num_rating)
        app_data_row.append(coef_1_5_num_rating)
        app_data_row.append(coef_2_5_num_rating)
        app_data_row.append(coef_3_5_num_rating)
        app_data_row.append(coef_avg_rating_num)

        coef_pos_neg_rating_csv.writerow(app_data_row)

    app_data_file.close()
    coef_pos_neg_rating.close()


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple'
    __date_pattern = '%m/%d/%y'

    generate_features(__data_path, __host, __user, __passwd, __db_name, __date_pattern)