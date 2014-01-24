from sklearn.ensemble import RandomForestClassifier
import csv
import numpy as np

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
target_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for app_data_row in appDataCsv:
    features_data.append([app_data_row[index] for index in feature_index])
    target_data.append(app_data_row[-1])

forest = RandomForestClassifier(random_state=0)
forest.fit(features_data, target_data)

importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
indices = np.argsort(importances)[::-1]

print(indices)

print("Feature ranking:")

for f in xrange(len(features)):
    print "%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]])

feature_list = [features[indices[f]] for f in xrange(37)]
print(feature_list)

import pylab as pl

pl.figure()
pl.title("Feature importances")
pl.bar(xrange(len(features)), importances[indices], color="r", align="center")
pl.xticks(xrange(len(features)), indices)
pl.xlim([-1, len(features)])
pl.show()