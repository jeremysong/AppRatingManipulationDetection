import ast
from collections import defaultdict
import MySQLdb
import matplotlib.pyplot as plt
import pylab
import numpy as np

__author__ = 'jeremy'


def consecutive_id(host, user, passwd, db_name, app_list, verbose=True):
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    raw_comment_data_sql = "SELECT reviewer_id FROM (SELECT reviewer_id, date FROM Comment WHERE app_id='{}' ORDER BY reviewer_id) as TEMP ORDER BY date;"

    def num_consecutive_id(__reviewer_id_list, __consecutive_range=1000):
        count = 0
        if len(__reviewer_id_list) <= 1:
            return count
        __reviewer_id_iter = iter(__reviewer_id_list)
        first_id = next(__reviewer_id_iter)
        for reviewer_id in __reviewer_id_iter:
            second_id = reviewer_id
            if abs(second_id - first_id) <= __consecutive_range:
                count += 1
            first_id = second_id
        return count

    coverage_list = list()
    num_consecutive_id_list = list()

    for abused_app_id in app_list:
        comment_data_sql = raw_comment_data_sql.replace('{}', abused_app_id)
        cur.execute(comment_data_sql)
        reviewer_ids = cur.fetchall()
        try:
            reviewer_id_list = [int(reviewer_id_row[0]) for reviewer_id_row in reviewer_ids]
        except TypeError:
            continue
        if len(reviewer_id_list) == 0:
            continue
        #reviewer_id_list.sort()
        num_consecutive_ids = num_consecutive_id(reviewer_id_list)
        coverage = num_consecutive_ids / float(len(reviewer_id_list))
        num_consecutive_id_list.append(num_consecutive_ids)
        coverage_list.append(coverage)

        if verbose and coverage >= 0.015:
            print('App id: {0}; num_consecutive_id: {1}; coverage: {2}'.format(abused_app_id, num_consecutive_ids,
                                                                               num_consecutive_ids / float(
                                                                                   len(reviewer_id_list))))

    coverage_90 = [coverage for coverage in coverage_list if coverage < 1.0]
    coverage_80 = [coverage for coverage in coverage_list if coverage < 0.9]
    coverage_70 = [coverage for coverage in coverage_list if coverage < 0.8]
    coverage_60 = [coverage for coverage in coverage_list if coverage < 0.7]
    coverage_50 = [coverage for coverage in coverage_list if coverage < 0.6]
    coverage_40 = [coverage for coverage in coverage_list if coverage < 0.5]
    coverage_30 = [coverage for coverage in coverage_list if coverage < 0.4]
    coverage_20 = [coverage for coverage in coverage_list if coverage < 0.3]
    coverage_10 = [coverage for coverage in coverage_list if coverage < 0.2]
    coverage_05 = [coverage for coverage in coverage_list if coverage < 0.1]
    coverage_04 = [coverage for coverage in coverage_list if coverage < 0.05]
    coverage_03 = [coverage for coverage in coverage_list if coverage < 0.04]
    coverage_02 = [coverage for coverage in coverage_list if coverage < 0.03]
    coverage_01 = [coverage for coverage in coverage_list if coverage < 0.02]
    coverage_00 = [coverage for coverage in coverage_list if coverage < 0.01]

    total_apps = float(len(coverage_list))

    return [len(coverage_00) / total_apps, len(coverage_01) / total_apps, len(coverage_02) / total_apps,
            len(coverage_03) / total_apps, len(coverage_04) / total_apps, len(coverage_05) / total_apps,
            len(coverage_10) / total_apps, len(coverage_20) / total_apps,
            len(coverage_30) / total_apps, len(coverage_40) / total_apps, len(coverage_50) / total_apps,
            len(coverage_60) / total_apps, len(coverage_70) / total_apps,
            len(coverage_80) / total_apps, len(coverage_90) / total_apps], coverage_list
    # return coverage_list, num_consecutive_id_list


def build_freq_dict(num_list):
    freq = defaultdict(int)
    for num in num_list:
        freq[int(num * 10000)] += 1

    x = sorted(freq.keys())
    y = [freq[k] for k in x]
    return x, y


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_uk_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_uk'

    suspicious_app_file = open(__data_path + 'classification_abused_app.txt', 'r')
    benign_app_file = open(__data_path + 'sample_total.csv', 'r')
    abused_app_file = open(__data_path + 'abused_apps.txt', 'r')

    suspicious_app_list = ast.literal_eval(next(suspicious_app_file))
    benign_app_list = [line.split(',')[0] for line in benign_app_file]
    abused_app_list = [line.split('.')[1].strip() for line in abused_app_file]

    suspicious_density = list()
    benign_density = list()
    abused_density = list()

    def consecutive_id_configured(__app_list, __verbose):
        return consecutive_id(__host, __user, __passwd, __db_name, __app_list, verbose=__verbose)

    # suspicious_coverage_list = consecutive_id_configured(suspicious_app_list, False)[1]
    # benign_coverage_list = consecutive_id_configured(benign_app_list, True)[1]
    # abused_coverage_list = consecutive_id_configured(abused_app_list, False)[1]

    # suspicious_x, suspicious_y = build_freq_dict(suspicious_coverage_list)
    # benign_x, benign_y = build_freq_dict(benign_coverage_list)
    # abused_x, abused_y = build_freq_dict(abused_coverage_list)

    # pylab.boxplot([suspicious_coverage_list, abused_coverage_list, benign_coverage_list])
    # pylab.grid()
    # pylab.xticks([1, 2, 3], ['Suspicious', 'Abused', 'Benign'])
    # pylab.show()

    x_axis = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    fig = plt.subplot()
    fig.plot(x_axis, consecutive_id_configured(suspicious_app_list, True)[0],
             label='Suspicious')
    fig.plot(x_axis, consecutive_id_configured(abused_app_list, True)[0],
             label='Abused')
    fig.plot(x_axis, consecutive_id_configured(benign_app_list, True)[0],
             label='Benign')
    fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(x_axis,
               ['<1%', '', '', '', '<5%', '<10%', '<20%', '<30%', '<40%', '<50%', '<60%', '<70%', '<80%',
                '<90%', '<100%'])
    plt.ylim([0.0, 1.1])
    plt.yticks(np.arange(0.0, 1.1, 0.1))
    plt.xlabel('Coverage of Consecutive IDs')
    plt.ylabel('Percentage of Apps')
    plt.grid()
    plt.show()
