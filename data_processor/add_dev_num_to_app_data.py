"""
Test this program before being used.
"""

import csv

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/updateTotalRaterAppData.csv", "r")
appDataCsv = csv.reader(appDataFile, delimiter=',')
preProcessedAppDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/devNumAppData.csv", "w")
preProcessedAppDataCsvWriter = csv.writer(preProcessedAppDataFile, delimiter=',')

developer_dict = dict()

appDataHeader = next(appDataCsv)

for app_data_row in appDataCsv:
    developer_name = app_data_row[9]
    if developer_name not in developer_dict:
        developer_dict[developer_name] = 1
    else:
        developer_dict[developer_name] += 1

# Reset appDataFile
appDataFile.seek(0)
next(appDataCsv)

appDataHeader[9] = "num_dev"
preProcessedAppDataCsvWriter.writerow(appDataHeader)

for app_data_row in appDataCsv:
    developer_name = app_data_row[9]
    app_data_row[9] = developer_dict[app_data_row[9]]
    preProcessedAppDataCsvWriter.writerow(app_data_row)

appDataFile.close()
preProcessedAppDataFile.close()