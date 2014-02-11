"""
Extreme positive rater: reviewers who rate more than 2 apps and only give 4 or 5 stars.
Extreme negative rater: reviewers who rate more than 2 apps and only give 1 or 2 stars.

Consider merging this file with add_pos_neg_rater_to_reviewer.py
"""

__author__ = 'jeremy'

import csv


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


def generate_features(data_path):
    reviewer_data_file = open(data_path + "posNegReviewerData.csv", "r")
    extr_pos_neg_reviewer_data_file = open(data_path + "extrPosNegReviewerData.csv", "w")

    reviewer_data_csv = csv.reader(reviewer_data_file, delimiter=',')
    extr_pos_neg_reviewer_data_csv = csv.writer(extr_pos_neg_reviewer_data_file, delimiter=',')

    reviewer_data_header = next(reviewer_data_csv)
    reviewer_data_header.extend(['extr_pos_rater', 'extr_neg_rater'])

    extr_pos_neg_reviewer_data_csv.writerow(reviewer_data_header)

    for reviewer_row in reviewer_data_csv:
        pos = extr_pos_rater(reviewer_row)
        neg = extr_neg_rater(reviewer_row)
        reviewer_row.append(pos)
        reviewer_row.append(neg)

        extr_pos_neg_reviewer_data_csv.writerow(reviewer_row)

    extr_pos_neg_reviewer_data_file.close()
    reviewer_data_file.close()
    print('Finish adding extreme positive and negative features to reviewer data.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    generate_features(__data_path)