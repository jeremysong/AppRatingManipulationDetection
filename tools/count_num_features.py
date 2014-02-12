"""
Count number of features(fields actually)
"""

__author__ = 'jeremy'

import csv

trainingData = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/amazon_cn_data/varVersionRatingAppData.csv", 'r')
trainingDataCsv = csv.reader(trainingData, delimiter=',')

header = next(trainingDataCsv)

print(len(header))

trainingData.close()