"""
Analysis the number of each rating vs the number of reviewers who leave comment for each rating
"""

import csv
import MySQLdb

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/appData.csv", "r")
appDataCsv = csv.reader(appDataFile, delimiter=",")

numRaterCommentFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/numRaterCommentAnalysis.csv", "w")
numRaterCommentCsv = csv.writer(numRaterCommentFile, delimiter=",")

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT app_id, rating FROM Comment"
cur.execute(comment_sql)

comment_dict = dict()

for comment_row in cur.fetchall():
    app_id = comment_row[0]
    rating = comment_row[1]
    if app_id not in comment_dict:
        comment_dict[app_id] = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    comment_dict[app_id][str(rating)] += 1

next(appDataCsv)

# Key: app id, Value: list of percentage for each rating
result_dict = dict()

numRaterCommentCsv.writerow(['app_id', 'rate_one_perc', 'rate_two_perc', 'rate_three_perc', 'rate_four_perc', 'rate_five_perc'])

for app_data_row in appDataCsv:
    app_id = app_data_row[0]
    rate_one = app_data_row[3]
    rate_two = app_data_row[4]
    rate_three = app_data_row[5]
    rate_four = app_data_row[6]
    rate_five = app_data_row[7]

    try:
        rate_one_percentage = comment_dict[app_id]['1'] / float(rate_one)
        rate_two_percentage = comment_dict[app_id]['2'] / float(rate_two)
        rate_three_percentage = comment_dict[app_id]['3'] / float(rate_three)
        rate_four_percentage = comment_dict[app_id]['4'] / float(rate_four)
        rate_five_percentage = comment_dict[app_id]['5'] / float(rate_five)
    except ZeroDivisionError:
        continue

    numRaterCommentCsv.writerow([app_id, rate_one_percentage, rate_two_percentage, rate_three_percentage,
                                 rate_four_percentage, rate_five_percentage])

