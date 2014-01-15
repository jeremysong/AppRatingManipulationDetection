__author__ = 'jeremy'

from sklearn import neighbors
from sklearn import cross_validation
import numpy as np
import csv
import random

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['perc_pos_rater', 'num_pos_rater', 'price', 'num_dev', 'total_rater', 'var_num_rating_by_week',
           'var_perc_4_star_rating_by_week', 'var_perc_5_star_rating_by_week', 'average_rating', 'num_week',
           'helpfulness_ratio_avg', 'var_perc_neg_rater_by_week', 'perc_neg_rater', 'perc_helpfulness',
           'poisson_first_peak', '5star_num', 'var_perc_pos_rater_by_week', 'poisson_last_peek', 'num_neg_rater',
           'var_perc_3_star_rating_by_week', 'var_perc_1_star_rating_by_week', '2star_num', '4star_num',
           'num_helpfulness', 'var_perc_2_star_rating_by_week', 'poisson_num_peaks', 'var_avg_rating_by_week',
           '3star_num', '1star_num']

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for n in range(1, 20, 1):
    for app_data_row in appDataCsv:
        features_data.append([float(app_data_row[index]) for index in feature_index])
        abused_data.append(int(app_data_row[-1]))

    random.seed()

    clf = neighbors.KNeighborsClassifier(n, 'uniform')
    cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2, random_state=random.randint(1, 1000))

    scores = cross_validation.cross_val_score(clf, np.array(features_data), np.array(abused_data), cv=cv, scoring='f1')

    print(n)
    print('Average score:', np.average(scores))