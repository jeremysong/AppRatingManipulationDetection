"""
Read app data from database and store them into a single file for faster access and process.
"""

__author__ = 'jeremy'

import MySQLdb
import csv


def generate_app_data(data_path, host, user, passwd, db_name):
    app_data_file = open(data_path + "appData.csv", "w")
    app_data_csv = csv.writer(app_data_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    app_data_sql = "SELECT app_id, average_rating, total_raters, 1star_num, 2star_num, 3star_num, 4star_num, 5star_num, price, Developer_name FROM AppData"
    cur.execute(app_data_sql)

    app_data_csv.writerow(['app_id', 'average_rating', 'total_rater', '1star_num', '2star_num', '3star_num', '4star_num', '5star_num', 'price', 'Developer_name'])

    for app_data_row in cur.fetchall():
        app_data_row_write = list(app_data_row)
        app_data_row_write[8] = 0 if app_data_row[8] == 'Free' else 1
        app_data_csv.writerow(app_data_row_write)

    app_data_file.close()
    print("Finish reading app data from database.")


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    generate_app_data(__data_path, __host, __user, __passwd, __db_name)