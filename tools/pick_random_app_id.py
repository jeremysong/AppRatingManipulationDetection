"""
Picks random apps from non-labeled app set.
"""

import csv
import random

iTunesDataFolder = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/amazon_us_data/'

appDataFile = open(iTunesDataFolder + "coefPosNegRatingsAppData.csv", "r")
abusedDataFile = open(iTunesDataFolder + "trainingData.csv", "r")
sampleDataFile = open(iTunesDataFolder + "sample_predict_apps.csv", "w")

appDataCsv = csv.reader(appDataFile, delimiter=',')
abusedDataCsv = csv.reader(abusedDataFile, delimiter=',')
sampleDataCsv = csv.writer(sampleDataFile, delimiter=',')

# Ignore header
next(appDataCsv)
next(abusedDataCsv)

appIdSet = set()
abusedAppIdSet = set()

for line in appDataCsv:
    appIdSet.add(line[0])

for line in abusedDataCsv:
    abusedAppIdSet.add(line[0])

benignAppIdSet = appIdSet - abusedAppIdSet
print("Residual: {0}; Training: {1}.".format(len(benignAppIdSet), len(abusedAppIdSet)))

randomAppId = random.sample(benignAppIdSet, len(benignAppIdSet))

count = 1
for appId in randomAppId:
    writerow = [str(count), appId]
    sampleDataCsv.writerow(writerow)
    count += 1

appDataFile.close()
abusedDataFile.close()
sampleDataFile.close()