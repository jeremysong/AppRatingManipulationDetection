"""
Rebuild reviewer data from Comment table and store them into a file for faster access and process. Use SSCursor to deal with large dataset.
"""

__author__ = 'jeremy'

import MySQLdb
import MySQLdb.cursors
import csv


def generate_reviewer_data(data_path, host, user, passwd, db_name):
    reviewer_data_file = open(data_path + "completeReviewerData.csv", "w")
    reviewer_data_csv = csv.writer(reviewer_data_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name,
                         cursorclass=MySQLdb.cursors.SSCursor)
    cur = db.cursor()
    comment_sql = "SELECT reviewer_id, app_id, date, rating FROM Comment"
    cur.execute(comment_sql)

    reviewer_dict = dict()

    for comment_row in cur:
        reviewer_id = comment_row[0]
        app_id = comment_row[1]
        date = str(comment_row[2]).split(' ')[0]
        rating = str(comment_row[3])
        if reviewer_id not in reviewer_dict:
            reviewer_dict[reviewer_id] = {"app_ids": [app_id], "dates": [date], "ratings": [rating]}
        else:
            reviewer_dict[reviewer_id]["app_ids"].append(app_id)
            reviewer_dict[reviewer_id]["dates"].append(date)
            reviewer_dict[reviewer_id]["ratings"].append(rating)

    reviewer_data_header = ["reviewer_id", "app_ids", "reviewer_ratings", "review_dates", "size"]
    reviewer_data_csv.writerow(reviewer_data_header)

    for reviewer_id in reviewer_dict:
        app_ids = '_'.join(reviewer_dict[reviewer_id]["app_ids"])
        review_ratings = '_'.join(reviewer_dict[reviewer_id]["ratings"])
        review_dates = '_'.join(reviewer_dict[reviewer_id]["dates"])
        size = len(reviewer_dict[reviewer_id]["app_ids"])

        reviewer_data_csv.writerow([reviewer_id, app_ids, review_ratings, review_dates, size])

    reviewer_data_file.close()
    print('Finish building complete reviewer data from database.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    generate_reviewer_data(__data_path, __host, __user, __passwd, __db_name)