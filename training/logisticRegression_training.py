__author__ = 'jeremy'

import csv
from sklearn.linear_model import LogisticRegression
import random
import numpy as np
from sklearn import cross_validation

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'var_num_rating_by_week', 'total_rater',
            'var_perc_4_star_rating_by_week', 'num_neg_rater', '4star_num', 'var_perc_5_star_rating_by_week',
            'var_avg_rating_by_week', 'num_week', 'perc_helpfulness', 'perc_neg_rater', 'var_perc_neg_rater_by_week',
            'var_perc_3_star_rating_by_week', 'helpfulness_ratio_avg', 'var_perc_2_star_rating_by_week',
            'var_perc_1_star_rating_by_week', 'num_dev', 'price', 'poisson_first_peak', 'poisson_last_peek',
            'var_perc_pos_rater_by_week', 'num_helpfulness', '1star_num', '5star_num', '3star_num', 'average_rating',
            'poisson_num_peaks', '2star_num']

for num_features in range(1, 30, 1):
    logistic = LogisticRegression()

    features_data = list()
    abused_data = list()

    feature_index = [appDataHeader.index(feature) for feature in features[0: num_features + 1]]

    for app_data_row in appDataCsv:
        features_data.append([float(app_data_row[index]) for index in feature_index])
        abused_data.append(int(app_data_row[-1]))

    random.seed()
    cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2,
                                       random_state=random.randint(1, 1000))
    scores = cross_validation.cross_val_score(logistic, np.array(features_data), np.array(abused_data), cv=cv, scoring='f1')
    print(np.average(scores))

    appDataFile.seek(0)
    next(appDataCsv)