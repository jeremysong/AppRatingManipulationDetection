"""
Add variance of percentage of positive and negative rater by week and normalized by app version.
"""

__author__ = 'jeremy'

import csv
from datetime import datetime
import MySQLdb
import numpy


def generate_feature(data_path, host, user, passwd, db_name, has_version=True):
    app_data_file = open(data_path + "posNegWeekAppData.csv", 'r')
    reviewer_data_file = open(data_path + "posNegReviewerData.csv", 'r')
    version_var_perc_pos_neg_rater_file = open(data_path + "varVersionPercPosNegRaterAppData.csv", 'w')

    app_data_csv = csv.reader(app_data_file, delimiter=',')
    reviewer_data_csv = csv.reader(reviewer_data_file, delimiter=',')
    version_var_perc_pos_neg_rater_csv = csv.writer(version_var_perc_pos_neg_rater_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT app_id, date, reviewer_id, device_version FROM Comment"
    cur.execute(comment_sql)

    reviewer_dict = dict()
    # Key: app_id; Value: {version: {week: [reviewer_id]}}
    comment_dict = dict()
    # Key: app_id; Value: {version: {week: [perc_pos_rater, perc_neg_rater]}
    comment_perc_rater_dict = dict()

    next(reviewer_data_csv)

    for reviewer_row in reviewer_data_csv:
        reviewer_dict[reviewer_row[0]] = {"pos_rater": int(reviewer_row[5]), "neg_rater": int(reviewer_row[6])}

    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        reviewer_id = comment_row[2]
        date = datetime.strptime(comment_row[1].split(' ')[0], '%m/%d/%y').date()
        # Amazon and Windows do not provide version data. To leverage version noises,
        # assume a month is a live cycle of app
        version = comment_row[3] if has_version else str(date.year) + '.' + str(date.month)
        iso_calendar = date.isocalendar()
        year = iso_calendar[0]
        nth_week = iso_calendar[1]
        week_key = str(year) + '.' + str(nth_week)
        if app_id not in comment_dict:
            comment_dict[app_id] = {version: {week_key: [reviewer_id]}}
        else:
            if version not in comment_dict[app_id]:
                comment_dict[app_id][version] = {week_key: [reviewer_id]}
            else:
                if week_key not in comment_dict[app_id][version]:
                    comment_dict[app_id][version][week_key] = [reviewer_id]
                else:
                    comment_dict[app_id][version][week_key].append(reviewer_id)

    for app_id_key in comment_dict:
        reviewer_version_dict = comment_dict[app_id_key]
        for version in reviewer_version_dict:
            reviewer_week_dict = reviewer_version_dict[version]
            for week_key in reviewer_week_dict:
                reviewer_id_list = reviewer_week_dict[week_key]
                pos_rater_count = 0
                neg_rater_count = 0
                reviewer_count = len(reviewer_id_list)
                for reviewer_id in reviewer_id_list:
                    try:
                        pos_rater_count += reviewer_dict[reviewer_id]["pos_rater"]
                        neg_rater_count += reviewer_dict[reviewer_id]["neg_rater"]
                    except KeyError:
                        print("Missing reviewer_id: ", reviewer_id)
                        continue
                perc_pos_neg_rater_dict = {"perc_pos_rater": pos_rater_count / float(reviewer_count),
                                           "perc_neg_rater": neg_rater_count / float(reviewer_count)}
                if app_id_key not in comment_perc_rater_dict:
                    comment_perc_rater_dict[app_id_key] = {version: {week_key: perc_pos_neg_rater_dict}}
                else:
                    if version not in comment_perc_rater_dict[app_id_key]:
                        comment_perc_rater_dict[app_id_key][version] = {week_key: perc_pos_neg_rater_dict}
                    else:
                        comment_perc_rater_dict[app_id_key][version][week_key] = perc_pos_neg_rater_dict

    app_data_header = next(app_data_csv)
    app_data_header.extend(["var_perc_pos_rater_by_week_by_version", "var_perc_neg_rater_by_week_by_version"])

    version_var_perc_pos_neg_rater_csv.writerow(app_data_header)

    for app_data_row in app_data_csv:
        app_id = app_data_row[0]
        perc_pos_rater_by_version = list()
        perc_neg_rater_by_version = list()
        pos_neg_perc_by_version = comment_perc_rater_dict[app_id]
        for version in pos_neg_perc_by_version:
            perc_pos_rater_by_week = list()
            perc_neg_rater_by_week = list()
            pos_neg_perc_by_week = pos_neg_perc_by_version[version]
            for week_key in pos_neg_perc_by_week:
                perc_neg_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_pos_rater"])
                perc_pos_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_neg_rater"])
            perc_pos_rater_by_version.append(numpy.var(perc_pos_rater_by_week))
            perc_neg_rater_by_version.append(numpy.var(perc_neg_rater_by_week))
        app_data_row.extend([numpy.average(perc_pos_rater_by_version), numpy.average(perc_neg_rater_by_version)])

        version_var_perc_pos_neg_rater_csv.writerow(app_data_row)

    app_data_file.close()
    reviewer_data_file.close()
    version_var_perc_pos_neg_rater_file.close()
    print('Finish adding variance of percentage of positive and negative rater by week by version.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    generate_feature(__data_path, __host, __user, __passwd, __db_name, has_version=True)