from sklearn.ensemble import ExtraTreesClassifier
import csv
import numpy as np

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appDataWithAbusedInfo.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)
features = appDataHeader[1:-1]

features_data = list()
target_data = list()

for app_data_row in appDataCsv:
    features_data.append(app_data_row[1: -1])
    target_data.append(app_data_row[-1])

forest = ExtraTreesClassifier(compute_importances=True, random_state=0)
forest.fit(features_data, target_data)

importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
indices = np.argsort(importances)[::-1]

print(indices)

print("Feature ranking:")

for f in xrange(29):
    print "%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]])

import pylab as pl
pl.figure()
pl.title("Feature importances")
pl.bar(xrange(29), importances[indices], color="r", yerr=std[indices], align="center")
pl.xticks(xrange(29), indices)
pl.xlim([-1, 29])
pl.show()