from sklearn.ensemble import RandomForestClassifier
import csv
import numpy as np

appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)
features = ['average_rating', 'total_rater', '1star_num', '2star_num', '3star_num', '4star_num', '5star_num',
            'price', 'num_dev', 'num_pos_rater', 'perc_pos_rater', 'num_neg_rater', 'perc_neg_rater',
            'helpfulness_ratio_avg', 'num_helpfulness', 'perc_helpfulness', 'var_num_rating_by_week',
            'var_avg_rating_by_week', 'var_perc_1_star_rating_by_week', 'var_perc_2_star_rating_by_week',
            'var_perc_3_star_rating_by_week', 'var_perc_4_star_rating_by_week', 'var_perc_5_star_rating_by_week',
            'var_perc_pos_rater_by_week', 'var_perc_neg_rater_by_week', 'num_week', 'poisson_num_peaks',
            'poisson_first_peak', 'poisson_last_peak', 'num_extr_pos_rater', 'perc_extr_pos_rater',
            'num_extr_neg_rater', 'perc_extr_neg_rater', 'num_pos_week', 'perc_pos_week', 'num_neg_week',
            'perc_neg_week', 'max_pos_week', 'perc_max_pos_week', 'max_neg_week', 'perc_max_neg_week',
            'var_perc_pos_rater_by_week_by_version', 'var_perc_neg_rater_by_week_by_version',
            'var_num_rating_by_week_by_version', 'var_avg_rating_by_week_by_version',
            'var_perc_1_star_rating_by_week_by_version', 'var_perc_2_star_rating_by_week_by_version',
            'var_perc_3_star_rating_by_week_by_version', 'var_perc_4_star_rating_by_week_by_version',
            'var_perc_5_star_rating_by_week_by_version', 'coef_pos_neg_rating_by_week', 'coef_1_5_rating_by_week',
            'coef_2_5_rating_by_week', 'coef_3_5_rating_by_week', 'coef_avg_rating_num_by_week']

features_data = list()
target_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    target_data.append(int(app_data_row[-1]))

forest = RandomForestClassifier(random_state=0, n_estimators=87, oob_score=True, min_samples_leaf=3)
forest.fit(features_data, target_data)

importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
indices = np.argsort(importances)

feature_ranking_name = list()

print(indices)

print("Feature ranking:")

for f in xrange(len(features)):
    feature_name = features[indices[f]]
    # replace rater to reviewer since we use reviewer instead of rater in paper(except total_rater)
    if not 'total_rater' == feature_name:
        feature_name = feature_name.replace('rater', 'reviewer')
    feature_ranking_name.append(feature_name)
    print "%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]])

feature_list = [features[indices[f]] for f in xrange(len(features))]
print(feature_list)

import pylab as pl

pl.figure(figsize=(8, 12))
pl.title("Feature Ranking By Importance")
pl.barh(range(1, len(features) + 1, 1), importances[indices], 0.6, color="r", align="center")
pl.yticks(range(1, len(features) + 1, 1), feature_ranking_name, size='medium')
pl.ylim(0, len(features) + 1)
pl.xlim(0.00, 0.20)
pl.grid(True)
pl.tight_layout()
pl.show()