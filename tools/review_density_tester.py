import ast
from collections import defaultdict
from datetime import datetime

import MySQLdb
import pylab


__author__ = 'jeremy'


def review_density(host, user, passwd, db_name, date_pattern, abused_app_id, density_threshold):
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    comment_sql = "SELECT date FROM Comment WHERE app_id=" + "'" + abused_app_id + "'"
    cur.execute(comment_sql)

    comment_by_week_dict = dict()

    for comment_row in cur.fetchall():
        date = datetime.strptime(str(comment_row[0]).split(" ")[0], date_pattern).date()
        iso_calendar = date.isocalendar()
        # Use ISO calendar year here. For example, for 2012-01-01, it will return 2011, 52, 7
        year = iso_calendar[0]
        nth_week = iso_calendar[1]
        week_key = str(year) + '.' + str(nth_week)

        if week_key not in comment_by_week_dict:
            comment_by_week_dict[week_key] = 1
        else:
            comment_by_week_dict[week_key] += 1

    num_rater = comment_by_week_dict.values()

    max_num_rater = max(num_rater)
    min_num_rater = min(num_rater)

    threshold = (1 - density_threshold) * (max_num_rater - min_num_rater)

    above_threshold = len([num for num in num_rater if num >= threshold])
    return above_threshold / float(len(num_rater))


def build_greq_dict(density_list):
    freq = defaultdict(int)
    for density_item in density_list:
        freq[int(density_item * 10000)] += 1

    x = sorted(freq.keys())
    y = [freq[k] for k in x]
    return x, y


if __name__ == "__main__":
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple'
    __date_pattern = '%m/%d/%y'

    suspicious_app_file = open('/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/classification_abused_app.txt', 'r')
    benign_app_file = open('/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/sample_total.csv', 'r')
    abused_app_file = open('/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/abused_apps.txt', 'r')

    suspicious_app_list = ast.literal_eval(next(suspicious_app_file))
    benign_app_list = [line.split(',')[0] for line in benign_app_file]
    abused_app_list = [line.split('.')[1].strip() for line in abused_app_file]

    suspicious_density = list()
    benign_density = list()
    abused_density = list()

    for __suspicious_app_id in suspicious_app_list:
        density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __suspicious_app_id, 0.05)
        suspicious_density.append(density)
        print('App id: {0}, density: {1}'.format(__suspicious_app_id, density))

    for __benign_app_id in benign_app_list:
        density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __benign_app_id, 0.05)
        benign_density.append(density)
        print('App id: {0}, density: {1}'.format(__benign_app_id, density))

    for __abused_app_id in abused_app_list:
        try:
            density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __abused_app_id, 0.05)
        except ValueError:
            continue
        abused_density.append(density)
        print('App id: {0}, density: {1}'.format(__abused_app_id, density))

    suspicious_density_x, suspicious_density_y = build_greq_dict(suspicious_density)
    benign_density_x, benign_density_y = build_greq_dict(benign_density)
    abused_density_x, abused_density_y = build_greq_dict(abused_density)

    pylab.boxplot([suspicious_density, abused_density, benign_density])
    pylab.grid()
    pylab.ylabel('Density')
    pylab.xticks([1, 2, 3], ['Suspicious', 'Abused', 'Benign'])
    pylab.show()