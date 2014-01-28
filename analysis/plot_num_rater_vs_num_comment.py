import csv
import matplotlib.pyplot as plt
import numpy as np

numRaterCommentFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/numRaterCommentAnalysis.csv", 'r')
numRaterCommentCsv = csv.reader(numRaterCommentFile, delimiter=',')

one_rating_percentage = list()
two_rating_percentage = list()
three_rating_percentage = list()
four_rating_percentage = list()
five_rating_percentage = list()

next(numRaterCommentCsv)

for row in numRaterCommentCsv:
    one_rating_percentage.append(float(row[1]))
    two_rating_percentage.append(float(row[2]))
    three_rating_percentage.append(float(row[3]))
    four_rating_percentage.append(float(row[4]))
    five_rating_percentage.append(float(row[5]))


one_rating_percentage = [percentage for percentage in one_rating_percentage if percentage < 1]
two_rating_percentage = [percentage for percentage in two_rating_percentage if percentage < 1]
three_rating_percentage = [percentage for percentage in three_rating_percentage if percentage < 1]
four_rating_percentage = [percentage for percentage in four_rating_percentage if percentage < 1]
five_rating_percentage = [percentage for percentage in five_rating_percentage if percentage < 1]

plt.bar(np.arange(1, 100, 1), five_rating_percentage[:99], align="center")
plt.show()