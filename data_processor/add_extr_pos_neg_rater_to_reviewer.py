"""
Extreme positive rater: reviewers who rate more than 2 apps and only give 4 or 5 stars.
Extreme negative rater: reviewers who rate more than 2 apps and only give 1 or 2 stars.
"""

__author__ = 'jeremy'

import csv

reviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/posNegReviewerData.csv", "r")
extrPosNegReviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/extrPosNegReviewerData.csv", "w")

reviewerDataCsv = csv.reader(reviewerDataFile, delimiter=',')
extrPosNegReviewerDataCsv = csv.writer(extrPosNegReviewerDataFile, delimiter=',')

reviewerDataHeader = next(reviewerDataCsv)
reviewerDataHeader.extend(['extr_pos_rater', 'extr_neg_rater'])

extrPosNegReviewerDataCsv.writerow(reviewerDataHeader)


def extr_pos_rater(row):
    ratings = row[2].split('_')
    ratings = map(int, ratings)
    if min(ratings) <= 3 or len(ratings) < 3:
        return 0
    else:
        return 1


def extr_neg_rater(row):
    ratings = row[2].split('_')
    ratings = map(int, ratings)
    if max(ratings) >= 3 or len(ratings) < 3:
        return 0
    else:
        return 1


for reviewer_row in reviewerDataCsv:
    pos = extr_pos_rater(reviewer_row)
    neg = extr_neg_rater(reviewer_row)
    reviewer_row.append(pos)
    reviewer_row.append(neg)

    extrPosNegReviewerDataCsv.writerow(reviewer_row)

extrPosNegReviewerDataFile.close()
reviewerDataFile.close()