"""
Test this program before being used.
"""

import csv


def generate_features(data_path):
    app_data_file = open(data_path + "appData.csv", "r")
    app_data_csv = csv.reader(app_data_file, delimiter=',')
    pre_processed_app_data_file = open(data_path + "devNumAppData.csv", "w")
    pre_processed_app_data_csv_writer = csv.writer(pre_processed_app_data_file, delimiter=',')

    developer_dict = dict()

    app_data_header = next(app_data_csv)

    for app_data_row in app_data_csv:
        developer_name = app_data_row[9]
        if developer_name not in developer_dict:
            developer_dict[developer_name] = 1
        else:
            developer_dict[developer_name] += 1

    # Reset appDataFile
    app_data_file.seek(0)
    next(app_data_csv)

    app_data_header[9] = "num_dev"
    pre_processed_app_data_csv_writer.writerow(app_data_header)

    for app_data_row in app_data_csv:
        app_data_row[9] = developer_dict[app_data_row[9]]
        pre_processed_app_data_csv_writer.writerow(app_data_row)

    app_data_file.close()
    pre_processed_app_data_file.close()
    print("Finish adding dev_num feature.")


if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    generate_features(__data_path)
