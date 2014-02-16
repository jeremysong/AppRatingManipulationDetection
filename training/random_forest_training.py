"""
Random forest training model.
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import numpy as np
import csv
import matplotlib.pylab as plt
import random
from sklearn.metrics import precision_recall_fscore_support


appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'total_rater', 'var_num_rating_by_week', 'perc_extr_pos_rater',
            'var_avg_rating_by_week', 'num_extr_pos_rater', 'num_pos_week', 'num_week', 'poisson_first_peak',
            'var_perc_5_star_rating_by_week', 'var_perc_1_star_rating_by_week', 'perc_max_pos_week',
            'perc_max_neg_week', 'num_neg_rater', 'perc_neg_week', 'perc_neg_rater', 'var_perc_4_star_rating_by_week',
            '2star_num', 'var_perc_2_star_rating_by_week', 'perc_helpfulness', 'poisson_last_peak',
            'var_perc_pos_rater_by_week', 'var_perc_3_star_rating_by_week', '3star_num', '4star_num',
            'var_perc_neg_rater_by_week', '1star_num', 'perc_pos_week', 'price', 'num_dev', 'max_pos_week',
            'helpfulness_ratio_avg', 'perc_extr_neg_rater', 'num_extr_neg_rater', 'num_helpfulness',
            'poisson_num_peaks', '5star_num', 'average_rating', 'num_neg_week', 'max_neg_week',
            'var_perc_pos_rater_by_week_by_version', 'var_perc_neg_rater_by_week_by_version',
            "var_num_rating_by_week_by_version", "var_avg_rating_by_week_by_version",
            "var_perc_1_star_rating_by_week_by_version", "var_perc_2_star_rating_by_week_by_version",
            "var_perc_3_star_rating_by_week_by_version", "var_perc_4_star_rating_by_week_by_version",
            "var_perc_5_star_rating_by_week_by_version", "coef_pos_neg_rating_by_week", "coef_1_5_rating_by_week",
            "coef_2_5_rating_by_week", "coef_3_5_rating_by_week", "coef_avg_rating_num_by_week"]

precision_score_collection = list()
recall_score_collection = list()
f1_score_collection = list()

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    abused_data.append(int(app_data_row[-1]))

random.seed()
cv = cross_validation.ShuffleSplit(len(features_data), n_iter=10, test_size=0.1,
                                   random_state=random.randint(1, 1000))

num_estimator_range = range(60, 100, 1)

for num_estimators in num_estimator_range:
    clf = RandomForestClassifier(n_estimators=num_estimators, oob_score=True, min_samples_leaf=4)

    score_collection = list()

    for train_index, test_index in cv:
        training_data = [features_data[idx] for idx in train_index]
        training_target = [abused_data[idx] for idx in train_index]
        test_data = [features_data[idx] for idx in test_index]
        test_target = [abused_data[idx] for idx in test_index]

        clf.fit(training_data, training_target)
        prediction = clf.predict(test_data)
        scores = precision_recall_fscore_support(test_target, prediction, pos_label=1)
        score_collection.append(scores)

    precision_score = np.average([scores[0][1] for scores in score_collection])
    recall_score = np.average([scores[1][1] for scores in score_collection])
    f1_score = np.average([scores[2][1] for scores in score_collection])
    print('Average precision: {0:f}. Average recall: {1:f}. Average f1: {2:f}'.format(
        np.average([scores[0][1] for scores in score_collection]),
        np.average([scores[1][1] for scores in score_collection]),
        np.average([scores[2][1] for scores in score_collection])))

    appDataFile.seek(0)
    next(appDataCsv)

    precision_score_collection.append(precision_score)
    recall_score_collection.append(recall_score)
    f1_score_collection.append(f1_score)
    # max_score = max(scores_by_feature)
    # index = scores_by_feature.index(max_score)
    # print(index, max_score)
    # plt.bar(np.arange(1, len(features), 1), scores_by_feature, align="center")
    # plt.show()

max_score = max(f1_score_collection)
min_score = min(f1_score_collection)
num_estimator = f1_score_collection.index(max_score)
print('Number of estimator: {0:d}. F1 --- Best score: {1:f}. Worst score: {2:f}. Average score: {3:f}'.format(
    num_estimator_range[num_estimator], max_score, min_score, np.average(f1_score_collection)))
print('Precision --- Best score: {0:f}. Worst score: {1:f}. Average score: {2:f}'.format(
    max(precision_score_collection), min(precision_score_collection), np.average(precision_score_collection)
))
print('Recall --- Best score: {0:f}. Worst score: {1:f}. Average score: {2:f}'.format(
    max(recall_score_collection), min(recall_score_collection), np.average(recall_score_collection)
))
plt.bar(num_estimator_range, f1_score_collection, align="center")
plt.xlim([num_estimator_range[0], num_estimator_range[-1]])
plt.show()
