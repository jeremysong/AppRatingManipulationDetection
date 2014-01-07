import codecs
import random

appDataFile = codecs.open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appData.csv", "r", encoding="utf-8")
abusedDataFile = codecs.open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/143465_abused_apps.txt", "r", encoding="utf-8")
sampleDataFile = codecs.open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/sample_apps.txt", "w")

# Ignore header
appDataFile.readline()
abusedDataFile.readline()

appIdSet = set()
abusedAppIdSet = set()


for line in appDataFile:
    appIdSet.add(line.split(",")[0])

for line in abusedDataFile:
    abusedAppIdSet.add(line.split(".")[0].strip())

benignAppIdSet = appIdSet - abusedAppIdSet

randomAppId = random.sample(benignAppIdSet, 400)

count = 1
for appId in randomAppId:
    sampleDataFile.write(str(count))
    sampleDataFile.write(",")
    sampleDataFile.write(appId)
    sampleDataFile.write("\n")
    count += 1

appDataFile.close()
abusedDataFile.close()
sampleDataFile.close()