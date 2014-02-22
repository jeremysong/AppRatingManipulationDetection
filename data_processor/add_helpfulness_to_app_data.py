"""
Add helpfulness features to app data
"""

__author__ = 'jeremy'

import csv
import MySQLdb


def generate_features(data_path, host, user, passwd, db_name):
    app_data_file = open(data_path + "posNegAppData.csv", "r")
    helpfulness_app_data_file = open(data_path + "helpfulnessAppData.csv", "w")
    app_data_csv = csv.reader(app_data_file, delimiter=',')
    pre_processed_app_data_csv_writer = csv.writer(helpfulness_app_data_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT app_id, helpfulness_ratio FROM Comment"
    cur.execute(comment_sql)

    comment_dict = dict()

    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        helpfulness_ratio = comment_row[1]
        if app_id not in comment_dict:
            comment_dict[app_id] = [helpfulness_ratio]
        else:
            comment_dict[app_id].append(helpfulness_ratio)

    app_data_header = next(app_data_csv)
    app_data_header.append("helpfulness_ratio_avg")
    app_data_header.append("num_helpfulness")
    app_data_header.append("perc_helpfulness")
    pre_processed_app_data_csv_writer.writerow(app_data_header)

    for app_row in app_data_csv:
        app_id = app_row[0]
        total_comments = len(comment_dict[app_id])
        helpfulness_sum = sum(comment_dict[app_id])
        avg_helpfulness = helpfulness_sum / total_comments
        helpful_count = 0
        for helpful_ratio in comment_dict[app_id]:
            if helpful_ratio > 0:
                helpful_count += 1
        perc_helpfulness = helpful_count / float(total_comments)
        app_row.append(avg_helpfulness)
        app_row.append(helpful_count)
        app_row.append(perc_helpfulness)
        pre_processed_app_data_csv_writer.writerow(app_row)

    app_data_file.close()
    helpfulness_app_data_file.close()

    print("Finish adding helpfulness features to app data.")


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'
    generate_features(__data_path, __host, __user, __passwd, __db_name)