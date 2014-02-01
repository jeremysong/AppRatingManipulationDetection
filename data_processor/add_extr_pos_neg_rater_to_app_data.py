"""
Add extreme positive rater and extreme negative rater to app data
"""

__author__ = 'jeremy'

import csv
import MySQLdb

appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/poissonAppData.csv", 'r')
reviewerDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/extrPosNegReviewerData.csv", 'r')
appDataWithExtrPosNegRaterFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/extrPosNegAppData.csv", 'w')

appDataCsv = csv.reader(appDataFile, delimiter=',')
reviewerDataCsv = csv.reader(reviewerDataFile, delimiter=',')
appDataWithExtrPosNegRaterCsv = csv.writer(appDataWithExtrPosNegRaterFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple_us")
cur = db.cursor()

appDataFileHeader = next(appDataCsv)
next(reviewerDataCsv)

reviewer_dict = dict()

for reviewer_row in reviewerDataCsv:
    reviewer_dict[reviewer_row[0]] = {"extr_pos_rater": int(reviewer_row[7]), "extr_neg_rater": int(reviewer_row[8])}

appDataFileHeader.extend(['num_extr_pos_rater', 'perc_extr_pos_rater', 'num_extr_neg_rater', 'perc_extr_neg_rater'])
appDataWithExtrPosNegRaterCsv.writerow(appDataFileHeader)

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

for app_data_row in appDataCsv:
    app_id = app_data_row[0]
    total_rater = len(comment_dict[app_id])
    extr_pos_rater = 0
    extr_neg_rater = 0
    for reviewer_id in comment_dict[app_id]:
        try:
            extr_pos_rater += int(reviewer_dict[reviewer_id]["extr_pos_rater"])
            extr_neg_rater += int(reviewer_dict[reviewer_id]["extr_neg_rater"])
        except KeyError:
            continue
    percent_extr_pos = extr_pos_rater / float(total_rater)
    percent_extr_neg = extr_neg_rater / float(total_rater)

    app_data_row.append(extr_pos_rater)
    app_data_row.append(percent_extr_pos)
    app_data_row.append(extr_neg_rater)
    app_data_row.append(percent_extr_neg)
    appDataWithExtrPosNegRaterCsv.writerow(app_data_row)

reviewerDataFile.close()
appDataFile.close()
appDataWithExtrPosNegRaterFile.close()