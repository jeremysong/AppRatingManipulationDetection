__author__ = 'jeremy'

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import ShuffleSplit
from sklearn.feature_selection import RFECV
import csv
import pylab as pl
import numpy as np

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

best_scores = list()

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features[0:]]

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    abused_data.append(int(app_data_row[-1]))

linear = LogisticRegression()
cv = ShuffleSplit(len(features_data), n_iter=5, test_size=0.2, random_state=0)
rfecv = RFECV(estimator=linear, step=1, cv=cv, scoring='f1')
rfecv.fit(np.array(features_data), np.array(abused_data))

print("Optimal number of features : %d" % rfecv.n_features_)
ranking = rfecv.ranking_

feature_selection = [features[index] for index in range(0, 20) if ranking[index] == 1]
print(feature_selection)

# Plot number of features VS. cross-validation scores
pl.figure()
pl.xlabel("Number of features selected")
pl.ylabel("Cross validation score (nb of misclassifications)")
pl.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
pl.show()
