__author__ = 'jeremy'

import csv
from sklearn.linear_model import LogisticRegression
import random
import numpy as np
from sklearn import cross_validation

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'total_rater', 'perc_pos_rater', 'var_perc_5_star_rating_by_week', 'num_dev',
            'num_neg_rater', 'perc_extr_pos_rater', 'var_perc_4_star_rating_by_week', 'perc_max_pos_week', '4star_num',
            'price', '3star_num', 'perc_pos_week', 'perc_neg_rater', 'perc_helpfulness', 'var_perc_neg_rater_by_week',
            'var_perc_3_star_rating_by_week', 'max_pos_week', 'num_week', 'var_avg_rating_by_week', 'num_pos_week',
            'perc_max_neg_week', 'perc_neg_week', 'var_perc_1_star_rating_by_week', 'average_rating',
            'perc_extr_neg_rater', 'var_perc_2_star_rating_by_week', 'var_perc_pos_rater_by_week', '1star_num',
            'poisson_num_peaks', 'num_neg_week', 'poisson_first_peak', 'poisson_last_peek', 'num_helpfulness',
            'num_extr_neg_rater', 'helpfulness_ratio_avg', '2star_num']

logistic = LogisticRegression()

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

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