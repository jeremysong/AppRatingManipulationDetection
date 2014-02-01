"""
Count number of features(fields actually)
"""

__author__ = 'jeremy'

import csv

trainingData = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/varVersionRatingAppData.csv", 'r')
trainingDataCsv = csv.reader(trainingData, delimiter=',')

header = next(trainingDataCsv)

print(len(header))

trainingData.close()