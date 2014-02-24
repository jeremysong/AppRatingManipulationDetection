import ast
from collections import defaultdict
from datetime import datetime

import MySQLdb
import pylab


__author__ = 'jeremy'


def review_density(host, user, passwd, db_name, date_pattern, abused_app_id):
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

    if len(num_rater) > 5:
        num_rater = num_rater[5:]

    max_num_rater = max(num_rater)
    total_week = len(num_rater)
    total_area = max_num_rater * total_week
    area = sum(num_rater)

    # return sum(i > threshold for i in num_rater) / float(len(num_rater))
    return area / float(total_area)


def build_freq_dict(density_list):
    freq = defaultdict(int)
    for density_item in density_list:
        freq[int(density_item * 10000)] += 1

    x = sorted(freq.keys())
    y = [freq[k] for k in x]
    return x, y


if __name__ == "__main__":
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __date_pattern = '%m/%d/%y'

    boxplotdata = list()
    for location, __db_name in [('itunes_us_data/', 'Crawler_apple_us'), ('itunes_cn_data/', 'Crawler_apple'),
                                ('itunes_uk_data/', 'Crawler_apple_uk')]:
        suspicious_app_file = open(__data_path + location + 'classification_abused_app.txt', 'r')
        benign_app_file = open(__data_path + location + 'sample_total.csv', 'r')
        abused_app_file = open(__data_path + location + 'abused_apps.txt', 'r')

        suspicious_app_list = ast.literal_eval(next(suspicious_app_file))
        benign_app_list = [line.split(',')[0] for line in benign_app_file]
        abused_app_list = [line.split('.')[1].strip() for line in abused_app_file]

        suspicious_density = list()
        benign_density = list()
        abused_density = list()
        for __suspicious_app_id in suspicious_app_list:
            density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __suspicious_app_id)
            suspicious_density.append(density)
            print('App id: {0}, density: {1}'.format(__suspicious_app_id, density))

        for __benign_app_id in benign_app_list:
            density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __benign_app_id)
            benign_density.append(density)
            print('App id: {0}, density: {1}'.format(__benign_app_id, density))

        for __abused_app_id in abused_app_list:
            try:
                density = review_density(__host, __user, __passwd, __db_name, __date_pattern, __abused_app_id)
            except ValueError:
                continue
            abused_density.append(density)
            print('App id: {0}, density: {1}'.format(__abused_app_id, density))

        boxplotdata.extend([suspicious_density, abused_density, benign_density])

    # suspicious_density_x, suspicious_density_y = build_greq_dict(suspicious_density)
    # benign_density_x, benign_density_y = build_greq_dict(benign_density)
    # abused_density_x, abused_density_y = build_greq_dict(abused_density)

    pylab.boxplot(boxplotdata)
    pylab.grid()
    pylab.ylabel('Density')
    pylab.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9],
                 ['US Suspicious', 'US Abused', 'US Benign', 'China Suspicious', 'China Abused', 'China Benign',
                  'UK Suspicious', 'UK Abused', 'UK Benign'])
    pylab.show()