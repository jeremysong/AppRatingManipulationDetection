"""
Builds training set from Poisson App Data file, abused data and sample total.
"""

__author__ = 'jeremy'

import csv

iTunesDataFolder = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'

appFeatureFile = open(iTunesDataFolder + 'varVersionRatingAppData.csv', 'r')
abusedAppFile = open(iTunesDataFolder + 'us_abused_apps.txt', 'r')
sampleAppDataFile = open(iTunesDataFolder + 'sample_total.csv', 'r')
trainingDataFile = open(iTunesDataFolder + 'trainingData.csv', 'w')

appFeatureCsv = csv.reader(appFeatureFile, delimiter=',')
abusedAppCsv = csv.reader(abusedAppFile, delimiter='.')
sampleAppDataCsv = csv.reader(sampleAppDataFile, delimiter=',')
trainingDataCsv = csv.writer(trainingDataFile, delimiter=',')

targetData = dict()

for abused_app_row in abusedAppCsv:
    targetData[abused_app_row[1].strip()] = 1

for sample_app_row in sampleAppDataCsv:
    targetData[sample_app_row[0]] = int(sample_app_row[1])

print(len(targetData))

trainingDataHeader = next(appFeatureCsv)
trainingDataHeader.append('target')
trainingDataCsv.writerow(trainingDataHeader)

for app_feature_row in appFeatureCsv:
    app_id = app_feature_row[0]
    if app_id in targetData:
        app_feature_row.append(targetData[app_id])
        trainingDataCsv.writerow(app_feature_row)
        targetData.pop(app_id)

appFeatureFile.close()
abusedAppFile.close()
sampleAppDataFile.close()
trainingDataFile.close()