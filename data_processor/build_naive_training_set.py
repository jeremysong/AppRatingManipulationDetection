"""
Builds naive training set. Apps in this training are identical to ones in the normal training set. But only label apps
that are in abused_apps.txt file.
"""

__author__ = 'jeremy'

import csv

iTunesDataFolder = '/Users/jeremy/Google Drive/PSU/thesis/itunes_data/'

appFeatureFile = open(iTunesDataFolder + 'poissonAppData.csv', 'r')
abusedAppFile = open(iTunesDataFolder + '143465_abused_apps.txt', 'r')
sampleAppDataFile = open(iTunesDataFolder + 'sample_total.csv', 'r')
naiveTrainingDataFile = open(iTunesDataFolder + 'naiveTrainingData.csv', 'w')

appFeatureCsv = csv.reader(appFeatureFile, delimiter=',')
abusedAppCsv = csv.reader(abusedAppFile, delimiter='.')
sampleAppDataCsv = csv.reader(sampleAppDataFile, delimiter=',')
naiveTrainingDataCsv = csv.writer(naiveTrainingDataFile, delimiter=',')

targetData = dict()

for abused_app_row in abusedAppCsv:
    targetData[abused_app_row[1].strip()] = 1

for sample_app_row in sampleAppDataCsv:
    targetData[sample_app_row[1]] = 0

print(len(targetData))

trainingDataHeader = next(appFeatureCsv)
trainingDataHeader.append('target')
naiveTrainingDataCsv.writerow(trainingDataHeader)

for app_feature_row in appFeatureCsv:
    app_id = app_feature_row[0]
    if app_id in targetData:
        app_feature_row.append(targetData[app_id])
        naiveTrainingDataCsv.writerow(app_feature_row)
        targetData.pop(app_id)

appFeatureFile.close()
abusedAppFile.close()
sampleAppDataFile.close()
naiveTrainingDataFile.close()