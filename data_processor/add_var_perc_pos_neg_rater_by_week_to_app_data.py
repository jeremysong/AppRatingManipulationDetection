import csv
from datetime import datetime
import MySQLdb
import numpy


def generate_features(data_path, host, user, passwd, db_name, date_pattern):
    app_data_file = open(data_path + "varRatingAppData.csv", "r")
    reviewer_data_file = open(data_path + "posNegReviewerData.csv", "r")
    var_perc_pos_neg_rater_file = open(data_path + "varPercPosNegRaterAppData.csv", "w")

    app_data_csv = csv.reader(app_data_file, delimiter=',')
    reviewer_data_csv = csv.reader(reviewer_data_file, delimiter=',')
    var_perc_pos_neg_rater_csv = csv.writer(var_perc_pos_neg_rater_file, delimiter=',')

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT app_id, date, reviewer_id FROM Comment"
    cur.execute(comment_sql)

    reviewer_dict = dict()
    comment_dict = dict()
    comment_perc_rater_dict = dict()

    next(reviewer_data_csv)

    for reviewer_row in reviewer_data_csv:
        reviewer_dict[reviewer_row[0]] = {"pos_rater": int(reviewer_row[5]), "neg_rater": int(reviewer_row[6])}

    for comment_row in cur.fetchall():
        app_id = comment_row[0]
        reviewer_id = comment_row[2]
        date = datetime.strptime(str(comment_row[1]).split(" ")[0], date_pattern).date()
        iso_calendar = date.isocalendar()
        year = iso_calendar[0]
        nth_week = iso_calendar[1]
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
                comment_perc_rater_dict[app_id_key] = {
                    week_key: {"perc_pos_rater": pos_rater_count / float(reviewer_count),
                               "perc_neg_rater": neg_rater_count / float(reviewer_count)}}
            else:
                comment_perc_rater_dict[app_id_key][week_key] = {
                    "perc_pos_rater": pos_rater_count / float(reviewer_count),
                    "perc_neg_rater": neg_rater_count / float(reviewer_count)}

    app_data_header = next(app_data_csv)
    app_data_header.append("var_perc_pos_rater_by_week")
    app_data_header.append("var_perc_neg_rater_by_week")
    app_data_header.append("num_week")

    var_perc_pos_neg_rater_csv.writerow(app_data_header)

    for app_data_row in app_data_csv:
        app_id = app_data_row[0]
        perc_pos_rater_by_week = list()
        perc_neg_rater_by_week = list()
        pos_neg_perc_by_week = comment_perc_rater_dict[app_id]
        num_week = len(pos_neg_perc_by_week)
        for week_key in pos_neg_perc_by_week:
            perc_pos_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_pos_rater"])
            perc_neg_rater_by_week.append(pos_neg_perc_by_week[week_key]["perc_neg_rater"])
        var_perc_pos_rater = numpy.var(perc_pos_rater_by_week)
        var_perc_neg_rater = numpy.var(perc_neg_rater_by_week)
        app_data_row.append(var_perc_pos_rater)
        app_data_row.append(var_perc_neg_rater)
        app_data_row.append(num_week)

        var_perc_pos_neg_rater_csv.writerow(app_data_row)

    app_data_file.close()
    reviewer_data_file.close()
    var_perc_pos_neg_rater_file.close()
    print('Finish adding variance of percentage of positive and negative rater by week.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'
    __date_pattern = '%m/%d/%y'

    generate_features(__data_path, __host, __user, __passwd, __db_name, __date_pattern)

