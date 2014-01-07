import csv
from datetime import datetime
import MySQLdb
import numpy

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/varRatingAppData.csv", "r")
reviewerDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/posNegReviewerData.csv", "r")
varPercPosNegRaterFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/varPercPosNegRaterAppData.csv", "w")

appDataCsv = csv.reader(appDataFile, delimiter=',')
reviewerDataCsv = csv.reader(reviewerDataFile, delimiter=',')
varPercPosNegRaterCsv = csv.writer(varPercPosNegRaterFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT app_id, date, reviewer_id FROM Comment"
cur.execute(comment_sql)

reviewer_dict = dict()
comment_dict = dict()
comment_perc_rater_dict = dict()

next(reviewerDataCsv)

for reviewer_row in reviewerDataCsv:
    reviewer_dict[reviewer_row[0]] = {"pos_rater": int(reviewer_row[5]), "neg_rater": int(reviewer_row[6])}

for comment_row in cur.fetchall():
    app_id = comment_row[0]
    reviewer_id = comment_row[2]
    date = datetime.strptime(comment_row[1].split(" ")[0], '%m/%d/%y').date()
    isoCalendar = date.isocalendar()
    year = isoCalendar[0]
    nth_week = isoCalendar[1]
    week_key = str(year) + '.' + str(nth_week)
    if app_id not in comment_dict:
        comment_dict[app_id] = {week_key: [reviewer_id]}
    else:
        if week_key not in comment_dict:
            comment_dict[app_id][week_key] = [reviewer_id]
        else:
            comment_dict[app_id][week_key].append(reviewer_id)

for app_id_key in comment_dict:
    reviewer_week_dict = comment_dict[app_id_key]
    for week_key in reviewer_week_dict:
        reviewer_id_list = reviewer_week_dict[week_key]
        pos_rater_count = 0
        neg_rater_count = 0
        reviewer_count = len(reviewer_id_list)
        for reviewer_id in reviewer_id_list:
            try:
                pos_rater_count += reviewer_dict[reviewer_id]["pos_rater"]
                neg_rater_count += reviewer_dict[reviewer_id]["neg_rater"]
            except KeyError:
                print("Missing reviewer_id: ", reviewer_id)
                continue
        if app_id_key not in comment_perc_rater_dict:
            comment_perc_rater_dict[app_id_key] = {week_key: {"perc_pos_rater": pos_rater_count / float(reviewer_count), "perc_neg_rater": neg_rater_count / float(reviewer_count)}}
        else:
            comment_perc_rater_dict[app_id_key][week_key] = {"perc_pos_rater": pos_rater_count / float(reviewer_count), "perc_neg_rater": neg_rater_count / float(reviewer_count)}

appDataHeader = next(appDataCsv)
appDataHeader.append("var_perc_pos_rater_by_week")
appDataHeader.append("var_perc_neg_rater_by_week")
appDataHeader.append("num_week")

varPercPosNegRaterCsv.writerow(appDataHeader)

for app_data_row in appDataCsv:
    app_id = app_data_row[0]
    perc_pos_rater_by_week = list()
    perc_neg_rater_by_week = list()
    pos_neg_perc_by_week = comment_perc_rater_dict[app_id]
    num_week = len(pos_neg_perc_by_week)
    for week_key in pos_neg_perc_by_week:
        perc_neg_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_pos_rater"])
        perc_pos_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_neg_rater"])
    var_perc_pos_rater = numpy.var(perc_pos_rater_by_week)
    var_perc_neg_rater = numpy.var(perc_neg_rater_by_week)
    app_data_row.append(var_perc_pos_rater)
    app_data_row.append(var_perc_neg_rater)
    app_data_row.append(num_week)

    varPercPosNegRaterCsv.writerow(app_data_row)

appDataFile.close()
reviewerDataFile.close()
varPercPosNegRaterFile.close()