import ast
import MySQLdb

__author__ = 'jeremy'

abusedAppFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/classification_abused_app.txt",
                     'r')

abused_app_list = ast.literal_eval(next(abusedAppFile))

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
appDataSql = "SELECT app_name, developer_name, sub_category FROM AppData WHERE app_id="

for abused_app_id in abused_app_list:
    app_data_sql = appDataSql + "'" + abused_app_id + "'"
    cur.execute(app_data_sql)
    abused_app_info = cur.fetchone()
    try:
        app_name = abused_app_info[0]
    except TypeError:
        continue
    developer_name = abused_app_info[1]
    print(
    "App id: {0}, app name: {1}, developer name: {2}, category: {3}.".format(abused_app_id, app_name, developer_name,
                                                                             abused_app_info[2]))