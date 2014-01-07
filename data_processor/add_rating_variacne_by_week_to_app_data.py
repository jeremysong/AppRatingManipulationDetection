import csv
import MySQLdb
from datetime import datetime
import numpy

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/helpfulnessAppData.csv", "r")
appDataFileCsvReader = csv.reader(appDataFile, delimiter=',')
varRatingAppDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/varRatingAppData.csv", "w")
varRatingAppDataCsvWriter = csv.writer(varRatingAppDataFile, delimiter=',')

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple")
cur = db.cursor()
comment_sql = "SELECT app_id, date, rating FROM Comment"
cur.execute(comment_sql)

# Key: app ID; Value: dictionary, whose key: yyyy.nth_week; value: list of ratings
comment_by_week_dict = dict()

for comment_row in cur.fetchall():
    app_id = comment_row[0]
    date = datetime.strptime(comment_row[1].split(" ")[0], '%m/%d/%y').date()
    rating = comment_row[2]
    isoCalendar = date.isocalendar()
    # Use ISO calendar year here. For example, for 2012-01-01, it will return 2011, 52, 7
    year = isoCalendar[0]
    nth_week = isoCalendar[1]
    week_key = str(year) + '.' + str(nth_week)
    if app_id not in comment_by_week_dict:
        comment_by_week_dict[app_id] = {week_key: [rating]}
    else:
        if week_key not in comment_by_week_dict[app_id]:
            comment_by_week_dict[app_id][week_key] = [rating]
        else:
            comment_by_week_dict[app_id][week_key].append(rating)

# App data header
appDataFileHeader = next(appDataFileCsvReader)
appDataFileHeader.append("var_num_rating_by_week")
appDataFileHeader.append("var_avg_rating_by_week")
appDataFileHeader.append("var_perc_1_star_rating_by_week")
appDataFileHeader.append("var_perc_2_star_rating_by_week")
appDataFileHeader.append("var_perc_3_star_rating_by_week")
appDataFileHeader.append("var_perc_4_star_rating_by_week")
appDataFileHeader.append("var_perc_5_star_rating_by_week")

varRatingAppDataCsvWriter.writerow(appDataFileHeader)

for app_data_row in appDataFileCsvReader:
    app_id = app_data_row[0]
    rating_week_dict = comment_by_week_dict[app_id]
    num_rating_by_week = list()
    avg_rating_by_week = list()
    perc_1_star_rating_by_week = list()
    perc_2_star_rating_by_week = list()
    perc_3_star_rating_by_week = list()
    perc_4_star_rating_by_week = list()
    perc_5_star_rating_by_week = list()
    for week_key in rating_week_dict:
        num_rating = len(rating_week_dict[week_key])
        perc_1_star_rating = rating_week_dict[week_key].count(1) / float(num_rating)
        perc_2_star_rating = rating_week_dict[week_key].count(2) / float(num_rating)
        perc_3_star_rating = rating_week_dict[week_key].count(3) / float(num_rating)
        perc_4_star_rating = rating_week_dict[week_key].count(4) / float(num_rating)
        perc_5_star_rating = rating_week_dict[week_key].count(5) / float(num_rating)
        num_rating_by_week.append(num_rating)
        avg_rating_by_week.append(numpy.average(rating_week_dict[week_key]))
        perc_1_star_rating_by_week.append(perc_1_star_rating)
        perc_2_star_rating_by_week.append(perc_2_star_rating)
        perc_3_star_rating_by_week.append(perc_3_star_rating)
        perc_4_star_rating_by_week.append(perc_4_star_rating)
        perc_5_star_rating_by_week.append(perc_5_star_rating)

    var_num_rating_by_week = numpy.var(num_rating_by_week)
    var_avg_rating_by_week = numpy.var(avg_rating_by_week)
    var_perc_1_star_rating_by_week = numpy.var(perc_1_star_rating_by_week)
    var_perc_2_star_rating_by_week = numpy.var(perc_2_star_rating_by_week)
    var_perc_3_star_rating_by_week = numpy.var(perc_3_star_rating_by_week)
    var_perc_4_star_rating_by_week = numpy.var(perc_4_star_rating_by_week)
    var_perc_5_star_rating_by_week = numpy.var(perc_5_star_rating_by_week)

    app_data_row.append(var_num_rating_by_week)
    app_data_row.append(var_avg_rating_by_week)
    app_data_row.append(var_perc_1_star_rating_by_week)
    app_data_row.append(var_perc_2_star_rating_by_week)
    app_data_row.append(var_perc_3_star_rating_by_week)
    app_data_row.append(var_perc_4_star_rating_by_week)
    app_data_row.append(var_perc_5_star_rating_by_week)

    varRatingAppDataCsvWriter.writerow(app_data_row)

appDataFile.close()
varRatingAppDataFile.close()