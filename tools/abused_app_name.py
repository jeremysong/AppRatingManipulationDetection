"""
show abused apps' names and developers' names
"""

__author__ = 'jeremy'

import csv
import MySQLdb

abusedAppFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/abused_apps.txt", 'r')
abusedAppCsv = csv.reader(abusedAppFile, delimiter='.')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
appDataSql = "SELECT app_name, developer_name FROM AppData WHERE app_id="

for abused_app_row in abusedAppCsv:
    app_id = abused_app_row[1].strip()
    app_data_sql = appDataSql + "'" + app_id + "'"
    cur.execute(app_data_sql)
    abused_app_info = cur.fetchone()
    try:
        app_name = abused_app_info[0]
    except TypeError:
        continue
    developer_name = abused_app_info[1]
    print(app_name)
    print(developer_name)

cur.close()
db.close()