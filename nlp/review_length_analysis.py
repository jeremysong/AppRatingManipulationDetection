"""
This program only works for english sentences.

I actually use Java Lucene to handle tokenize problem as it could tokenize complex sentences(such as English + Chinese)
automatically. Lucene also could filter out punctuations in different languages.
"""

import ast
import MySQLdb
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy

__author__ = 'jeremy'


def tokenization(host, user, passwd, db_name, data_path):
    #benign_app_file = open(data_path + 'sample_total.csv', 'r')
    abused_app_file = open(data_path + 'abused_apps.txt', 'r')
    app_data = open(data_path + 'coefPosNegRatingsAppData.csv', 'r')
    suspicious_app_file = open(data_path + 'classification_abused_app.txt', 'r')

    next(app_data)

    #benign_app_list = list()
    abused_app_list = list()
    total_app_set = set()

    # for benign_row in benign_app_file:
    #     benign_app_list.append(benign_row.split(',')[0])

    for app_data_row in app_data:
        total_app_set.add(app_data_row.split(',')[0])

    for abused_row in abused_app_file:
        abused_app_list.append(abused_row.split('.')[1].strip())

    abused_app_list.extend(ast.literal_eval(next(suspicious_app_file)))

    benign_app_list = list(set(total_app_set) - set(abused_app_list))

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()
    app_data_sql_raw = "SELECT comment, comment_title FROM Comment WHERE app_id='{}'"

    benign_app_comment_list = list()
    abused_app_comment_list = list()

    for app_id in benign_app_list:
        app_data_sql = app_data_sql_raw.replace('{}', app_id)
        cur.execute(app_data_sql)
        for comment_row in cur.fetchall():
            benign_app_comment_list.append(comment_row[0] + ' ' + comment_row[1])

    for app_id in abused_app_list:
        app_data_sql = app_data_sql_raw.replace('{}', app_id)
        cur.execute(app_data_sql)
        for comment_row in cur.fetchall():
            abused_app_comment_list.append(comment_row[0] + ' ' + comment_row[1])

    benign_app_comment_num_token = [len(word_tokenize(comment)) for comment in benign_app_comment_list]
    abused_app_comment_num_token = [len(word_tokenize(comment)) for comment in abused_app_comment_list]

    return numpy.average(benign_app_comment_num_token), numpy.average(abused_app_comment_num_token)


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'

    # us_benign, us_abused = tokenization(host=__host, user=__user, passwd=__passwd, db_name='Crawler_apple_us',
    #                                     data_path=__data_path + 'itunes_us_data/')
    # uk_benign, uk_abused = tokenization(host=__host, user=__user, passwd=__passwd, db_name='Crawler_apple_uk',
    #                                     data_path=__data_path + 'itunes_uk_data/')

    ###################################################
    ## DO NOT DELETE THIS, THIS IS IMPORTANT RESULTS ##
    ###################################################
    us_benign, us_abused = (23.773304, 13.012153)
    uk_benign, uk_abused = (26.974686, 15.896525)
    cn_benign, cn_abused = (12.3986635, 12.651336)

    fig = plt.subplot()
    fig.set_ylabel('Average Number of Tokens')
    abused = fig.bar(numpy.arange(1, 4, 1) - 0.2, [us_abused, uk_abused, cn_abused], color='r', width=0.2)
    benign = fig.bar(numpy.arange(1, 4, 1), [us_benign, uk_benign, cn_benign], color='b', width=0.2)
    fig.legend([abused, benign], ['Abused App', 'Benign App'], loc=2)
    plt.xlim(0, 4)
    plt.xticks([1, 2, 3], ['US', 'UK', 'China'])
    plt.grid()
    plt.show()