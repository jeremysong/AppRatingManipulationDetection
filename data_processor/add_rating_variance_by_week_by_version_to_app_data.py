"""
Add Rating variance by week normalized by version. For iTunes only.
"""

import csv
import MySQLdb
from datetime import datetime
import numpy as np

__author__ = 'jeremy'


def generate_features(data_path, host, user, passwd, db_name, date_pattern, has_version=True):
    app_data_file = open(data_path + "varVersionPercPosNegRaterAppData.csv", 'r')
    var_version_rating_app_data_file = open(data_path + "varVersionRatingAppData.csv", 'w')

    app_data_file_csv = csv.reader(app_data_file, delimiter=',')
    var_version_rating_csv = csv.writer(var_version_rating_app_data_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT app_id, date, rating, device_version FROM Comment"
    cur.execute(comment_sql)

    # key: app_id, value: {version: {week_key: [ratings]}}
    comment_by_version_dict = dict()

    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        date = datetime.strptime(str(comment_row[1]).split(' ')[0], date_pattern).date()
        rating = comment_row[2]
        # Amazon and Windows do not provide version data. To leverage version noises,
        # assume a month is a live cycle of app
        version = comment_row[3] if has_version else str(date.year) + '.' + str(date.month)
        iso_calendar = date.isocalendar()
        year = iso_calendar[0]
        nth_week = iso_calendar[1]
        week_key = str(year) + '.' + str(nth_week)
        if app_id not in comment_by_version_dict:
            comment_by_version_dict[app_id] = {version: {week_key: [rating]}}
        else:
            if version not in comment_by_version_dict[app_id]:
                comment_by_version_dict[app_id][version] = {week_key: [rating]}
            else:
                if week_key not in comment_by_version_dict[app_id][version]:
                    comment_by_version_dict[app_id][version][week_key] = [rating]
                else:
                    comment_by_version_dict[app_id][version][week_key].append(rating)

    #App data header
    app_data_file_header = next(app_data_file_csv)
    app_data_file_header.extend(["var_num_rating_by_week_by_version", "var_avg_rating_by_week_by_version",
                                 "var_perc_1_star_rating_by_week_by_version",
                                 "var_perc_2_star_rating_by_week_by_version",
                                 "var_perc_3_star_rating_by_week_by_version",
                                 "var_perc_4_star_rating_by_week_by_version",
                                 "var_perc_5_star_rating_by_week_by_version"])

    var_version_rating_csv.writerow(app_data_file_header)

    for app_data_row in app_data_file_csv:
        app_id = app_data_row[0]
        rating_version_dict = comment_by_version_dict[app_id]
        num_rating_by_version = list()
        avg_rating_by_version = list()
        perc_1_star_rating_by_version = list()
        perc_2_star_rating_by_version = list()
        perc_3_star_rating_by_version = list()
        perc_4_star_rating_by_version = list()
        perc_5_star_rating_by_version = list()
        for version in rating_version_dict:
            rating_week_dict = rating_version_dict[version]
            num_rating_by_week = list()
            avg_rating_by_week = list()
            perc_1_star_rating_by_week = list()
            perc_2_star_rating_by_week = list()
            perc_3_star_rating_by_week = list()
            perc_4_star_rating_by_week = list()
            perc_5_star_rating_by_week = list()
            for week_key in rating_week_dict:
                num_rating = len(rating_week_dict[week_key])
                perc_1_star_rating = rating_week_dict[week_key].count(1) / float(num_rating)
                perc_2_star_rating = rating_week_dict[week_key].count(2) / float(num_rating)
                perc_3_star_rating = rating_week_dict[week_key].count(3) / float(num_rating)
                perc_4_star_rating = rating_week_dict[week_key].count(4) / float(num_rating)
                perc_5_star_rating = rating_week_dict[week_key].count(5) / float(num_rating)
                num_rating_by_week.append(num_rating)
                avg_rating_by_week.append(np.average(rating_week_dict[week_key]))
                perc_1_star_rating_by_week.append(perc_1_star_rating)
                perc_2_star_rating_by_week.append(perc_2_star_rating)
                perc_3_star_rating_by_week.append(perc_3_star_rating)
                perc_4_star_rating_by_week.append(perc_4_star_rating)
                perc_5_star_rating_by_week.append(perc_5_star_rating)

            num_rating_by_version.append(np.var(num_rating_by_week))
            avg_rating_by_version.append(np.var(avg_rating_by_week))
            perc_1_star_rating_by_version.append(np.var(perc_1_star_rating_by_week))
            perc_2_star_rating_by_version.append(np.var(perc_2_star_rating_by_week))
            perc_3_star_rating_by_version.append(np.var(perc_3_star_rating_by_week))
            perc_4_star_rating_by_version.append(np.var(perc_4_star_rating_by_week))
            perc_5_star_rating_by_version.append(np.var(perc_5_star_rating_by_week))

        app_data_row.append(np.average(num_rating_by_version))
        app_data_row.append(np.average(avg_rating_by_version))
        app_data_row.append(np.average(perc_1_star_rating_by_version))
        app_data_row.append(np.average(perc_2_star_rating_by_version))
        app_data_row.append(np.average(perc_3_star_rating_by_version))
        app_data_row.append(np.average(perc_4_star_rating_by_version))
        app_data_row.append(np.average(perc_5_star_rating_by_version))

        var_version_rating_csv.writerow(app_data_row)

    app_data_file.close()
    var_version_rating_app_data_file.close()
    print('Finish adding rating variance by week by version features.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'
    __date_pattern = '%m/%d/%y'

    generate_features(__data_path, __host, __user, __passwd, __db_name, __date_pattern, has_version=True)