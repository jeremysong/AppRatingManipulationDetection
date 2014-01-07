"""
Rebuild reviewer data from Comment table in Crawler_apple database
"""

import MySQLdb
import csv

reviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/completeReviewerData.csv", "w")
reviewerDataCsv = csv.writer(reviewerDataFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT reviewer_id, app_id, date, rating FROM Comment"
cur.execute(comment_sql)

reviewer_dict = dict()

for comment_row in cur.fetchall():
    reviewer_id = comment_row[0]
    app_id = comment_row[1]
    date = comment_row[2].split(' ')[0]
    rating = str(comment_row[3])
    if reviewer_id not in reviewer_dict:
        reviewer_dict[reviewer_id] = {"app_ids": [app_id], "dates": [date], "ratings": [rating]}
    else:
        reviewer_dict[reviewer_id]["app_ids"].append(app_id)
        reviewer_dict[reviewer_id]["dates"].append(date)
        reviewer_dict[reviewer_id]["ratings"].append(rating)

reviewerDataHeader = ["reviewer_id", "app_ids", "reviewer_ratings", "review_dates", "size"]
reviewerDataCsv.writerow(reviewerDataHeader)

for reviewer_id in reviewer_dict:
    app_ids = '_'.join(reviewer_dict[reviewer_id]["app_ids"])
    review_ratings = '_'.join(reviewer_dict[reviewer_id]["ratings"])
    review_dates = '_'.join(reviewer_dict[reviewer_id]["dates"])
    size = len(reviewer_dict[reviewer_id]["app_ids"])

    reviewerDataCsv.writerow([reviewer_id, app_ids, review_ratings, review_dates, size])

reviewerDataFile.close()