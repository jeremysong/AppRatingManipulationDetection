import csv

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/varPercPosNegRaterAppData.csv", "r")
abusedAppFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/143465_abused_apps.txt", "r")
appDataWithAbusedInfoFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appDataWithAbusedInfo.csv", "w")

appDataCsv = csv.reader(appDataFile, delimiter=',')
abusedDataCsv = csv.reader(abusedAppFile, delimiter='.')
appDataWithAbusedInfoWriter = csv.writer(appDataWithAbusedInfoFile, delimiter=',')

appDataHeader = next(appDataCsv)
appDataHeader.append("abused")

appDataWithAbusedInfoWriter.writerow(appDataHeader)

abused_app_set = set()

for abused_app_row in abusedDataCsv:
    abused_app_set.add(abused_app_row[1].strip())

for app_data_row in appDataCsv:
    app_id = app_data_row[0]
    if app_id in abused_app_set:
        app_data_row.append(1)
    else:
        app_data_row.append(0)

    appDataWithAbusedInfoWriter.writerow(app_data_row)

appDataFile.close()
abusedAppFile.close()
appDataWithAbusedInfoFile.close()