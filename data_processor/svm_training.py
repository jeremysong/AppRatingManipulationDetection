from sklearn import svm
from sklearn import cross_validation
import csv
import numpy as np

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appDataWithAbusedInfo.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

next(appDataCsv)

features_data = list()
abused_data = list()

for app_data_row in appDataCsv:
    features_data.append(app_data_row[2: -2])
    abused_data.append(app_data_row[-1])

clf = svm.SVC(kernel='linear', C=1)
scores = cross_validation.cross_val_score(clf, np.array(features_data[:80]), np.array(abused_data[:80]), cv=3)

print("Finish training")

print(scores)
