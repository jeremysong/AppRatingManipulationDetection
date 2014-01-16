"""
n_estimator = 18, num of feature = 23, 0.92
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import numpy as np
import csv
import matplotlib.pylab as plt
import random
from sklearn.metrics import precision_recall_fscore_support

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/naiveTrainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'var_num_rating_by_week', 'total_rater',
            'var_perc_4_star_rating_by_week', 'num_neg_rater', '4star_num', 'var_perc_5_star_rating_by_week',
            'var_avg_rating_by_week', 'num_week', 'perc_helpfulness', 'perc_neg_rater', 'var_perc_neg_rater_by_week',
            'var_perc_3_star_rating_by_week', 'helpfulness_ratio_avg', 'var_perc_2_star_rating_by_week',
            'var_perc_1_star_rating_by_week', 'num_dev', 'price', 'poisson_first_peak', 'poisson_last_peek',
            'var_perc_pos_rater_by_week', 'num_helpfulness', '1star_num', '5star_num', '3star_num', 'average_rating',
            'poisson_num_peaks', '2star_num']

f1_score_collection = list()

for num_estimators in range(20, 100, 1):
    #for num_features in range(1, len(features), 1):
    for num_features in [29]:
        features_data = list()
        abused_data = list()

        feature_index = [appDataHeader.index(feature) for feature in features[0: num_features]]

        for app_data_row in appDataCsv:
            features_data.append([float(app_data_row[index]) for index in feature_index])
            abused_data.append(int(app_data_row[-1]))

        clf = RandomForestClassifier(n_estimators=num_estimators, max_features='log2')

        random.seed()
        cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2,
                                           random_state=random.randint(1, 1000))

        score_collection = list()

        for train_index, test_index in cv:
            training_data = [features_data[idx] for idx in train_index]
            training_target = [abused_data[idx] for idx in train_index]
            test_data = [features_data[idx] for idx in test_index]
            test_target = [abused_data[idx] for idx in test_index]

            clf.fit(training_data, training_target)
            prediction = clf.predict(test_data)
            scores = precision_recall_fscore_support(test_target, prediction)
            score_collection.append(scores)

        f1_score = np.average([scores[2] for scores in score_collection])
        print('Average precision: {0:f}. Average recall: {1:f}. Average f1: {2:f}'.format(
            np.average([scores[0] for scores in score_collection]),
            np.average([scores[1] for scores in score_collection]),
            np.average([scores[2] for scores in score_collection])))

        appDataFile.seek(0)
        next(appDataCsv)

        f1_score_collection.append(f1_score)
        # max_score = max(scores_by_feature)
        # index = scores_by_feature.index(max_score)
        # print(index, max_score)
        # plt.bar(np.arange(1, len(features), 1), scores_by_feature, align="center")
        # plt.show()

max_score = max(f1_score_collection)
min_score = min(f1_score_collection)
num_estimator = f1_score_collection.index(max_score)
print('Number of estimator: {0:d}. Best score: {1:f}. Worst score: {2:f}. Average score: {3:f}'.format(
    num_estimator + 1, max_score, min_score, np.average(f1_score_collection)))
plt.bar(range(20, 100, 1), f1_score_collection, align="center")
plt.xlim([20, 100])
plt.show()
