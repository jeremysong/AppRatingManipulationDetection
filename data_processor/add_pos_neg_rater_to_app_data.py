"""
Notes that the total_raters in AppData is not accurate. So get this number from Comment table.
"""

__author__ = 'jeremy'

import MySQLdb
import csv


def generate_features(data_path, host, user, passwd, db_name):
    app_data_file = open(data_path + "devNumAppData.csv", "r")
    reviewer_data_file = open(data_path + "posNegReviewerData.csv", "r")
    app_data_with_pos_neg_rater_file = open(data_path + "posNegAppData.csv", "w")

    app_data_csv = csv.reader(app_data_file, delimiter=',')
    reviewer_data_csv = csv.reader(reviewer_data_file, delimiter=',')
    app_data_with_pos_neg_rater_csv = csv.writer(app_data_with_pos_neg_rater_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()

    app_data_file_header = next(app_data_csv)
    next(reviewer_data_csv)

    reviewer_dict = dict()

    for reviewer_row in reviewer_data_csv:
        reviewer_dict[reviewer_row[0]] = {"pos_rater": int(reviewer_row[5]), "neg_rater": int(reviewer_row[6])}

    app_data_file_header.append('num_pos_rater')
    app_data_file_header.append('perc_pos_rater')
    app_data_file_header.append('num_neg_rater')
    app_data_file_header.append('perc_neg_rater')
    app_data_with_pos_neg_rater_csv.writerow(app_data_file_header)

    comment_dict = dict()
    comment_sql = "SELECT app_id, reviewer_id FROM Comment"
    cur.execute(comment_sql)
    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        reviewer_id = comment_row[1]
        if app_id not in comment_dict:
            comment_dict[app_id] = set(reviewer_id)
        else:
            comment_dict[app_id].add(reviewer_id)

    for app_data_row in app_data_csv:
        app_id = app_data_row[0]
        total_rater = len(comment_dict[app_id])
        pos_rater = 0
        neg_rater = 0
        for reviewer_id in comment_dict[app_id]:
            try:
                pos_rater += int(reviewer_dict[reviewer_id]["pos_rater"])
                neg_rater += int(reviewer_dict[reviewer_id]["neg_rater"])
            except KeyError:
                continue
        percent_pos = pos_rater / float(total_rater)
        percent_neg = neg_rater / float(total_rater)

        app_data_row.append(str(pos_rater))
        app_data_row.append(str(percent_pos))
        app_data_row.append(str(neg_rater))
        app_data_row.append(str(percent_neg))
        app_data_with_pos_neg_rater_csv.writerow(app_data_row)

    app_data_file.close()
    reviewer_data_file.close()
    app_data_with_pos_neg_rater_file.close()
    print('Finish adding positive and negative reviewer features.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    generate_features(__data_path, __host, __user, __passwd, __db_name)