"""
Notes that the total_raters in AppData is not accurate. So get this number from Comment table.
"""

import MySQLdb
import csv

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/devNumAppData.csv", "r")
reviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/posNegReviewerData.csv", "r")
appDataWithPosNegRaterFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/posNegAppData.csv", "w")

appDataCsv = csv.reader(appDataFile, delimiter=',')
reviewerDataCsv = csv.reader(reviewerDataFile, delimiter=',')
appDataWithPosNegRaterCsv = csv.writer(appDataWithPosNegRaterFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple_us")
cur = db.cursor()

appDataFileHeader = next(appDataCsv)
next(reviewerDataCsv)

reviewer_dict = dict()

for reviewer_row in reviewerDataCsv:
    reviewer_dict[reviewer_row[0]] = {"pos_rater": int(reviewer_row[5]), "neg_rater": int(reviewer_row[6])}

appDataFileHeader.append('num_pos_rater')
appDataFileHeader.append('perc_pos_rater')
appDataFileHeader.append('num_neg_rater')
appDataFileHeader.append('perc_neg_rater')
appDataWithPosNegRaterCsv.writerow(appDataFileHeader)

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
    appDataWithPosNegRaterCsv.writerow(app_data_row)

appDataFile.close()
reviewerDataFile.close()
appDataWithPosNegRaterFile.close()
