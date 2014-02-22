"""
Builds training set from Poisson App Data file, abused data and sample total.

Clean coefPosNegRatingAppData.csv file first as this file may contains lots of 'nan' data while coefficients are
generated.
I tried to use
    if np.isnan(coef)
to filter out those nan data, but it does not work. What I do is using substitution in vim.

To clean 'nan' for 'ceef_avg_rating_num_by_week' feature, substitute 'nan's with 0.0.
To clean other 'nan's, substitute them with 1.0.
"""

__author__ = 'jeremy'

import csv


def generate_training_set(data_path):
    app_feature_file = open(data_path + 'coefPosNegRatingsAppData.csv', 'r')
    abused_app_file = open(data_path + 'abused_apps.txt', 'r')
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
        try:
            target_data[sample_app_row[0]] = int(sample_app_row[1])
        except IndexError:
            print(sample_app_data_csv.line_num)
        if sample_app_data_csv.line_num == 1000:
            break

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
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/'
    generate_training_set(__data_path)
