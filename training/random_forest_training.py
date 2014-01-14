"""
n_estimator = 10, num of featuer = 24
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import numpy as np
import csv
import matplotlib.pylab as plt
import random

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

# features = ['perc_pos_rater', 'var_num_rating_by_week', 'num_pos_rater', 'total_rater', 'num_week', 'num_dev',
#             'var_perc_pos_rater_by_week', 'num_neg_rater', 'poisson_last_peak', 'var_perc_5_star_rating_by_week',
#             'var_avg_rating_by_week', 'var_perc_3_star_rating_by_week', 'var_perc_neg_rater_by_week',
#             'var_perc_1_star_rating_by_week', 'perc_neg_rater', 'poisson_first_peak', 'var_perc_2_star_rating_by_week',
#             'var_perc_4_star_rating_by_week', 'average_rating', 'num_helpfulness', 'perc_helpfulness',
#             'helpfulness_ratio_avg', '3star_num', 'poisson_num_peaks', '1star_num', '5star_num', '2star_num',
#             '4star_num', 'price']

features = ['perc_pos_rater', 'num_pos_rater', 'price', 'num_dev', 'total_rater', 'var_num_rating_by_week',
           'var_perc_4_star_rating_by_week', 'var_perc_5_star_rating_by_week', 'average_rating', 'num_week',
           'helpfulness_ratio_avg', 'var_perc_neg_rater_by_week', 'perc_neg_rater', 'perc_helpfulness',
           'poisson_first_peak', '5star_num', 'var_perc_pos_rater_by_week', 'poisson_last_peek', 'num_neg_rater',
           'var_perc_3_star_rating_by_week', 'var_perc_1_star_rating_by_week', '2star_num', '4star_num',
           'num_helpfulness', 'var_perc_2_star_rating_by_week', 'poisson_num_peaks', 'var_avg_rating_by_week',
           '3star_num', '1star_num']

best_scores = list()

for num_estimators in range(1, 20, 1):
#for num_estimators in [10]:
    scores_by_feature = list()
    for num_features in range(1, len(features), 1):
        features_data = list()
        abused_data = list()

        feature_index = [appDataHeader.index(feature) for feature in features[0: num_features]]

        for app_data_row in appDataCsv:
            features_data.append([float(app_data_row[index]) for index in feature_index])
            abused_data.append(int(app_data_row[-1]))

        clf = RandomForestClassifier(n_estimators=9)

        random.seed()
        cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2, random_state=random.randint(1, 1000))
        scores = cross_validation.cross_val_score(clf, np.array(features_data), np.array(abused_data), cv=cv, scoring='f1')

        print(scores)
        print('Average score:', np.average(scores))
        scores_by_feature.append(np.average(scores))

        appDataFile.seek(0)
        next(appDataCsv)

    best_scores.append(max(scores_by_feature))
    # max_score = max(scores_by_feature)
    # index = scores_by_feature.index(max_score)
    # print(index, max_score)
    # plt.bar(np.arange(1, len(features), 1), scores_by_feature, align="center")
    # plt.show()

max_score = max(best_scores)
num_estimator = best_scores.index(max_score)
print(num_estimator, max_score)
plt.bar(np.arange(1, 20, 1), best_scores, align="center")
plt.show()