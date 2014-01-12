"""
Add Poisson distribution features to App Data
"""

__author__ = 'jeremy'

import csv
from training import poission_dist_fitting as pdf

appDataFile = open('/Users/jeremy/Google Drive/PSU/thesis/itunes_data/varPercPosNegRaterAppData.csv', 'r')
poissonAppDataFile = open('/Users/jeremy/Google Drive/PSU/thesis/itunes_data/poissonAppData.csv', 'w')

appDataCsv = csv.reader(appDataFile, delimiter=',')
poissonAppDataCsv = csv.writer(poissonAppDataFile, delimiter=',')

appDataHeader = next(appDataCsv)
appDataHeader.extend(['poisson_num_peaks', 'poisson_first_peak', 'poisson_last_peak'])
poissonAppDataCsv.writerow(appDataHeader)

for app_data_row in appDataCsv:
    app_id = app_data_row[0]
    l_params, num_week = pdf.get_fitting_parameters(app_id)
    num_peaks = len(l_params)
    if not l_params:
        first_peak = 0
        last_peek = 0
        print('Cannot fit comment data', app_id)
    else:
        first_peak = min(l_params) / float(num_week)
        last_peek = max(l_params) / float(num_week)
    app_data_row.extend([num_peaks, first_peak, last_peek])

    poissonAppDataCsv.writerow(app_data_row)

appDataFile.close()
poissonAppDataFile.close()