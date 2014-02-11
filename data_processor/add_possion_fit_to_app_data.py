"""
Add Poisson distribution features to App Data
"""

__author__ = 'jeremy'

import csv
from training import poission_dist_fitting as pdf


def generate_features(data_path, host, user, passwd, db_name):
    app_data_file = open(data_path + 'varPercPosNegRaterAppData.csv', 'r')
    poisson_app_data_file = open(data_path + 'poissonAppData.csv', 'w')

    app_data_csv = csv.reader(app_data_file, delimiter=',')
    poisson_app_data_csv = csv.writer(poisson_app_data_file, delimiter=',')

    app_data_header = next(app_data_csv)
    app_data_header.extend(['poisson_num_peaks', 'poisson_first_peak', 'poisson_last_peak'])
    poisson_app_data_csv.writerow(app_data_header)

    for app_data_row in app_data_csv:
        app_id = app_data_row[0]
        l_params, num_week = pdf.get_fitting_parameters(app_id, host, user, passwd, db_name)
        num_peaks = len(l_params)
        if not l_params:
            first_peak = 0
            last_peek = 0
            print('Cannot fit comment data', app_id)
        else:
            first_peak = min(l_params) / float(num_week)
            last_peek = max(l_params) / float(num_week)
        app_data_row.extend([num_peaks, first_peak, last_peek])

        poisson_app_data_csv.writerow(app_data_row)

    app_data_file.close()
    poisson_app_data_file.close()


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    generate_features(__data_path, __host, __user, __passwd, __db_name)