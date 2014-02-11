"""
Add positive and negative features to reviewer

Consider merging this file with add_extr_pos_neg_rater_to_reviewer.py
"""

__author__ = 'jeremy'

import csv


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


def generate_features(data_path):
    reviewer_data_file = open(data_path + "completeReviewerData.csv", "r")
    pos_neg_reviewer_data_file = open(data_path + "posNegReviewerData.csv", "w")

    reviewer_data_csv = csv.reader(reviewer_data_file, delimiter=',')
    pos_neg_reviewer_data_csv = csv.writer(pos_neg_reviewer_data_file, delimiter=',')

    # header
    reviewer_data_header = next(reviewer_data_csv)
    reviewer_data_header.append("pos_rater")
    reviewer_data_header.append("neg_rater")

    pos_neg_reviewer_data_csv.writerow(reviewer_data_header)

    for reviewer_row in reviewer_data_csv:
        pos = pos_rater(reviewer_row)
        neg = neg_rater(reviewer_row)
        reviewer_row.append(pos)
        reviewer_row.append(neg)

        pos_neg_reviewer_data_csv.writerow(reviewer_row)

    reviewer_data_file.close()
    pos_neg_reviewer_data_file.close()
    print('Finish adding positive and negative rater feature to reviewer data.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    generate_features(__data_path)