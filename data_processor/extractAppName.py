import csv
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
app_data_sql = "SELECT app_name FROM AppData WHERE app_id="

sampleAppFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/sample_apps.txt", "r")
appNameFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/sample_apps_with_name.csv", "w")

sampleAppCsv = csv.reader(sampleAppFile, delimiter=",")
appNameCsv = csv.writer(appNameFile, delimiter=",")

appNameCsv.writerow(["id", "app_id", "app_name"])

for app_data_row in sampleAppCsv:
    app_id = app_data_row[1]
    cur.execute(app_data_sql + '"' + app_id + '"')
    app_data = cur.fetchone()
    app_data_row.append(app_data[0])
    appNameCsv.writerow(app_data_row)

sampleAppFile.close()
appNameFile.close()