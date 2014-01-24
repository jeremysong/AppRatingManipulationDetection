import csv
import MySQLdb

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/posNegAppData.csv", "r")
helpfulnessAppDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_us_data/helpfulnessAppData.csv", "w")
appDataCsv = csv.reader(appDataFile, delimiter=',')
preProcessedAppDataCsvWriter = csv.writer(helpfulnessAppDataFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple_us")
cur = db.cursor()
comment_sql = "SELECT app_id, helpfulness_ratio FROM Comment"
cur.execute(comment_sql)

comment_dict = dict()

for comment_row in cur.fetchall():
    app_id = comment_row[0]
    helpfulness_ratio = comment_row[1]
    if app_id not in comment_dict:
        comment_dict[app_id] = [helpfulness_ratio]
    else:
        comment_dict[app_id].append(helpfulness_ratio)

appDataHeader = next(appDataCsv)
appDataHeader.append("helpfulness_ratio_avg")
appDataHeader.append("num_helpfulness")
appDataHeader.append("perc_helpfulness")
preProcessedAppDataCsvWriter.writerow(appDataHeader)

for app_row in appDataCsv:
    app_id = app_row[0]
    total_comments = len(comment_dict[app_id])
    helpfulness_sum = sum(comment_dict[app_id])
    avg_helpfulness = helpfulness_sum / total_comments
    helpful_count = 0
    for helpful_ratio in comment_dict[app_id]:
        if helpful_ratio > 0:
            helpful_count += 1
    perc_helpfulness = helpful_count / float(total_comments)
    app_row.append(avg_helpfulness)
    app_row.append(helpful_count)
    app_row.append(perc_helpfulness)
    preProcessedAppDataCsvWriter.writerow(app_row)

appDataFile.close()
helpfulnessAppDataFile.close()