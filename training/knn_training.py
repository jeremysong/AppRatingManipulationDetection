__author__ = 'jeremy'

from sklearn import neighbors
from sklearn import cross_validation
import numpy as np
import csv
import random

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/itunes_cn_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'total_rater', 'var_num_rating_by_week', 'perc_extr_pos_rater',
            'var_avg_rating_by_week', 'num_extr_pos_rater', 'num_pos_week', 'num_week', 'poisson_first_peak',
            'var_perc_5_star_rating_by_week', 'var_perc_1_star_rating_by_week', 'perc_max_pos_week',
            'perc_max_neg_week', 'num_neg_rater', 'perc_neg_week', 'perc_neg_rater', 'var_perc_4_star_rating_by_week',
            '2star_num', 'var_perc_2_star_rating_by_week', 'perc_helpfulness', 'poisson_last_peek',
            'var_perc_pos_rater_by_week', 'var_perc_3_star_rating_by_week', '3star_num', '4star_num',
            'var_perc_neg_rater_by_week', '1star_num', 'perc_pos_week', 'price', 'num_dev', 'max_pos_week',
            'helpfulness_ratio_avg', 'perc_extr_neg_rater', 'num_extr_neg_rater', 'num_helpfulness',
            'poisson_num_peaks', '5star_num', 'average_rating', 'num_neg_week', 'max_neg_week',
            'var_perc_pos_rater_by_week_by_version', 'var_perc_neg_rater_by_week_by_version',
            "var_num_rating_by_week_by_version", "var_avg_rating_by_week_by_version",
            "var_perc_1_star_rating_by_week_by_version", "var_perc_2_star_rating_by_week_by_version",
            "var_perc_3_star_rating_by_week_by_version", "var_perc_4_star_rating_by_week_by_version",
            "var_perc_5_star_rating_by_week_by_version"]

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for n in range(1, 20, 1):
    for app_data_row in appDataCsv:
        features_data.append([float(app_data_row[index]) for index in feature_index])
        abused_data.append(int(app_data_row[-1]))

    random.seed()

    clf = neighbors.KNeighborsClassifier(n, 'uniform')
    cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2,
                                       random_state=random.randint(1, 1000))

    scores = cross_validation.cross_val_score(clf, np.array(features_data), np.array(abused_data), cv=cv, scoring='f1')

    print(n)
    print('Average score:', np.average(scores))