"""
Random forest training model.
"""

__author__ = 'jeremy'

import random
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support


appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['poisson_num_peaks', 'average_rating', 'num_extr_neg_rater', 'num_neg_week', '1star_num', 'num_dev',
            'max_neg_week', 'perc_max_neg_week', 'var_perc_2_star_rating_by_week_by_version', 'poisson_first_peak',
            'perc_neg_rater', 'max_pos_week', 'var_perc_2_star_rating_by_week', 'var_perc_pos_rater_by_week',
            'poisson_last_peak', 'perc_extr_neg_rater', 'num_helpfulness', '4star_num', '3star_num',
            'var_perc_4_star_rating_by_week_by_version', 'perc_pos_week', 'var_perc_pos_rater_by_week_by_version',
            '2star_num', 'var_perc_3_star_rating_by_week_by_version', 'perc_max_pos_week',
            'var_avg_rating_by_week_by_version', 'coef_2_5_rating_by_week', 'perc_neg_week', '5star_num',
            'var_perc_4_star_rating_by_week', 'var_perc_neg_rater_by_week_by_version', 'var_perc_5_star_rating_by_week',
            'var_perc_1_star_rating_by_week', 'var_perc_1_star_rating_by_week_by_version', 'num_neg_rater', 'price',
            'num_pos_week', 'helpfulness_ratio_avg', 'var_perc_5_star_rating_by_week_by_version',
            'var_perc_neg_rater_by_week', 'var_perc_3_star_rating_by_week', 'var_avg_rating_by_week',
            'coef_pos_neg_rating_by_week', 'coef_3_5_rating_by_week', 'perc_helpfulness', 'num_week',
            'coef_1_5_rating_by_week', 'num_pos_rater', 'coef_avg_rating_num_by_week', 'num_extr_pos_rater',
            'var_num_rating_by_week', 'perc_extr_pos_rater', 'total_rater', 'var_num_rating_by_week_by_version',
            'perc_pos_rater']

numline = sum(1 for line in appDataFile)
appDataFile.seek(0)
next(appDataCsv)
cv = cross_validation.ShuffleSplit(numline, n_iter=5, test_size=0.2, random_state=random.randint(0, 10000))
overall_best_evaluation = list()

feature_range = range(len(features), 9, -1)

for n_features in feature_range:
    precision_score_collection = list()
    recall_score_collection = list()
    f1_score_collection = list()
    num_estimator_collection = list()

    features_data = list()
    abused_data = list()
    selected_features = features[-n_features:]
    print('Feature length: {0}'.format(len(selected_features)))

    feature_index = [appDataHeader.index(feature) for feature in selected_features]

    for app_data_row in appDataCsv:
        features_data.append([float(app_data_row[index]) for index in feature_index])
        abused_data.append(int(app_data_row[-1]))

    num_estimator_range = range(61, 99, 2)

    for num_estimators in num_estimator_range:
        clf = RandomForestClassifier(n_estimators=num_estimators, oob_score=True, min_samples_leaf=3)

        score_collection = list()

        for train_index, test_index in cv:
            training_data = [features_data[idx] for idx in train_index]
            training_target = [abused_data[idx] for idx in train_index]
            test_data = [features_data[idx] for idx in test_index]
            test_target = [abused_data[idx] for idx in test_index]

            clf.fit(training_data, training_target)
            prediction = clf.predict(test_data)
            scores = precision_recall_fscore_support(test_target, prediction, pos_label=1, average='micro')
            score_collection.append(scores)

        precision_score = np.average([scores[0] for scores in score_collection])
        recall_score = np.average([scores[1] for scores in score_collection])
        f1_score = np.average([scores[2] for scores in score_collection])
        # print('Average precision: {0:f}. Average recall: {1:f}. Average f1: {2:f}'.format(
        #     np.average([scores[0][1] for scores in score_collection]),
        #     np.average([scores[1][1] for scores in score_collection]),
        #     np.average([scores[2][1] for scores in score_collection])))

        appDataFile.seek(0)
        next(appDataCsv)

        precision_score_collection.append(precision_score)
        recall_score_collection.append(recall_score)
        f1_score_collection.append(f1_score)
        num_estimator_collection.append(num_estimators)
        # max_score = max(scores_by_feature)
        # index = scores_by_feature.index(max_score)
        # print(index, max_score)
        # plt.bar(np.arange(1, len(features), 1), scores_by_feature, align="center")
        # plt.show()

    max_score = max(f1_score_collection)
    # min_score = min(f1_score_collection)
    max_index = f1_score_collection.index(max_score)
    max_n_estimator = num_estimator_collection[max_index]
    max_precision = precision_score_collection[max_index]
    max_recall = recall_score_collection[max_index]

    score_tuple = (max_precision, max_recall, max_score, max_n_estimator)
    print(score_tuple)
    overall_best_evaluation.append(score_tuple)
    # print('Number of estimator: {0:d}. F1 --- Best score: {1:f}. Worst score: {2:f}. Average score: {3:f}'.format(
    #     num_estimator_range[num_estimator], max_score, min_score, np.average(f1_score_collection)))
    # print('Precision --- Best score: {0:f}. Worst score: {1:f}. Average score: {2:f}'.format(
    #     max(precision_score_collection), min(precision_score_collection), np.average(precision_score_collection)
    # ))
    # print('Recall --- Best score: {0:f}. Worst score: {1:f}. Average score: {2:f}'.format(
    #     max(recall_score_collection), min(recall_score_collection), np.average(recall_score_collection)
    # ))

precision_score_overall = [overall[0] for overall in overall_best_evaluation]
recall_score_overall = [overall[1] for overall in overall_best_evaluation]
f1_score_overall = [overall[2] for overall in overall_best_evaluation]

fig = plt.subplot()
fig.plot(feature_range, precision_score_overall, label='precision')
fig.plot(feature_range, recall_score_overall, label='recall')
fig.plot(feature_range, f1_score_overall, label='f-score')
fig.set_ylabel('Scores')
fig.set_xlabel('Top N Features')
fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.grid()
plt.show()
