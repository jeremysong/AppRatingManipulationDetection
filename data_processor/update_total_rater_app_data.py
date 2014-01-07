import csv
import MySQLdb

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appData.csv", "r")
appDataUpdatedTotalRaterFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/updateTotalRaterAppData.csv", "w")

appDataCsv = csv.reader(appDataFile, delimiter=',')
appDataUpdatedTotalRaterCsv = csv.writer(appDataUpdatedTotalRaterFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT COUNT(*) FROM Comment WHERE app_id="

appDataHeader = next(appDataCsv)
appDataUpdatedTotalRaterCsv.writerow(appDataHeader)

for app_row in appDataCsv:
    app_id = app_row[0]
    cur.execute(comment_sql + '"' + app_id + '"')
    total_rater_row = cur.fetchone()
    app_row[2] = total_rater_row[0]
    appDataUpdatedTotalRaterCsv.writerow(app_row)

appDataFile.close()
appDataUpdatedTotalRaterFile.close()