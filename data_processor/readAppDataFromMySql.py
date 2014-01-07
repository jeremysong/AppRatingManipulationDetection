import MySQLdb
import csv

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appData.csv", "w")
appDataCsv = csv.writer(appDataFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
appDataSql = "SELECT app_id, average_rating, total_raters, 1star_num, 2star_num, 3star_num, 4star_num, 5star_num, price, Developer_name FROM AppData"
cur.execute(appDataSql)

appDataCsv.writerow(['app_id', 'average_rating', 'total_rater', '1star_num', '2star_num', '3star_num', '4star_num', '5star_num', 'price', 'Developer_name'])

for app_data_row in cur.fetchall():
    app_data_row_write = list(app_data_row)
    app_data_row_write[8] = 0 if app_data_row[8] == 'Free' else 1
    appDataCsv.writerow(app_data_row_write)

appDataFile.close()