import csv

reviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/completeReviewerData.csv", "r")
posNegReviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/posNegReviewerData.csv", "w")

reviewerDataCsv = csv.reader(reviewerDataFile, delimiter=',')
posNegReviewerDataCsv = csv.writer(posNegReviewerDataFile, delimiter=',')

# header
reviewerDataHeader = next(reviewerDataCsv)
reviewerDataHeader.append("pos_rater")
reviewerDataHeader.append("neg_rater")


def pos_rater(row):
    ratings = row[2].split('_')
    ratings = map(int, ratings)
    if min(ratings) <= 3:
        return 0
    else:
        return 1


def neg_rater(row):
    ratings = row[2].split('_')
    ratings = map(int, ratings)
    if max(ratings) >= 3:
        return 0
    else:
        return 1

posNegReviewerDataCsv.writerow(reviewerDataHeader)

for reviewer_row in reviewerDataCsv:
    pos = pos_rater(reviewer_row)
    neg = neg_rater(reviewer_row)
    reviewer_row.append(pos)
    reviewer_row.append(neg)

    posNegReviewerDataCsv.writerow(reviewer_row)

reviewerDataFile.close()
posNegReviewerDataFile.close()