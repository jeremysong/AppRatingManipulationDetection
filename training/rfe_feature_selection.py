__author__ = 'jeremy'

from sklearn.svm import LinearSVC
from sklearn.cross_validation import ShuffleSplit
from sklearn.feature_selection import RFECV
import csv
import pylab as pl
import numpy as np

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'var_num_rating_by_week', 'total_rater', 'perc_pos_rater', 'num_extr_pos_rater',
            'var_perc_5_star_rating_by_week', 'num_dev', 'num_neg_rater', 'perc_extr_pos_rater',
            'var_perc_4_star_rating_by_week', 'perc_max_pos_week', '4star_num', 'price', '3star_num', 'perc_pos_week',
            'perc_neg_rater', 'perc_helpfulness', 'var_perc_neg_rater_by_week', 'var_perc_3_star_rating_by_week',
            'max_pos_week', 'num_week', 'var_avg_rating_by_week', 'num_pos_week', 'perc_max_neg_week', 'perc_neg_week',
            'var_perc_1_star_rating_by_week', 'average_rating', 'perc_extr_neg_rater', 'var_perc_2_star_rating_by_week',
            'var_perc_pos_rater_by_week', '1star_num', 'poisson_num_peaks', 'num_neg_week', 'poisson_first_peak',
            'poisson_last_peek', 'num_helpfulness', 'num_extr_neg_rater', 'helpfulness_ratio_avg', '2star_num',
            '5star_num', 'max_neg_week']

best_scores = list()

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features[0:]]

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    abused_data.append(int(app_data_row[-1]))

linear = LinearSVC()
cv = ShuffleSplit(len(features_data), n_iter=5, test_size=0.2, random_state=0)
rfecv = RFECV(estimator=linear, step=1, cv=cv, scoring='f1')
rfecv.fit(np.array(features_data), np.array(abused_data))

print("Optimal number of features : %d" % rfecv.n_features_)
ranking = rfecv.ranking_
print(ranking)

feature_selection = [features[index] for index in range(0, len(features)-1) if ranking[index] == 1]
print(feature_selection)

# Plot number of features VS. cross-validation scores
pl.figure()
pl.xlabel("Number of features selected")
pl.ylabel("Cross validation score (nb of misclassifications)")
pl.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
pl.show()
