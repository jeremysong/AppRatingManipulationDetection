"""
Builds training set from Poisson App Data file, abused data and sample total.
"""

__author__ = 'jeremy'

import csv


def generate_training_set(data_path):
    app_feature_file = open(data_path + 'varVersionRatingAppData.csv', 'r')
    abused_app_file = open(data_path + 'us_abused_apps.txt', 'r')
    sample_app_data_file = open(data_path + 'sample_total.csv', 'r')
    training_data_file = open(data_path + 'trainingData.csv', 'w')

    app_feature_csv = csv.reader(app_feature_file, delimiter=',')
    abused_app_csv = csv.reader(abused_app_file, delimiter='.')
    sample_app_data_csv = csv.reader(sample_app_data_file, delimiter=',')
    training_data_csv = csv.writer(training_data_file, delimiter=',')

    target_data = dict()

    for abused_app_row in abused_app_csv:
        target_data[abused_app_row[1].strip()] = 1

    for sample_app_row in sample_app_data_csv:
        target_data[sample_app_row[0]] = int(sample_app_row[1])

    print(len(target_data))

    training_data_header = next(app_feature_csv)
    training_data_header.append('target')
    training_data_csv.writerow(training_data_header)

    for app_feature_row in app_feature_csv:
        app_id = app_feature_row[0]
        if app_id in target_data:
            app_feature_row.append(target_data[app_id])
            training_data_csv.writerow(app_feature_row)
            target_data.pop(app_id)

    app_feature_file.close()
    abused_app_file.close()
    sample_app_data_file.close()
    training_data_file.close()
    print('Finish building training set.')


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    generate_training_set(__data_path)
