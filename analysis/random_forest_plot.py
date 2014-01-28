"""
Plot tree for random forest training model
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import csv
import StringIO
import pydot
import random

appDataFile = open("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/trainingData.csv", 'r')
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

num_estimator = 60

feature_index = [appDataHeader.index(feature) for feature in features]

features_data = list()
abused_data = list()

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    abused_data.append(int(app_data_row[-1]))

random.seed()

clf = RandomForestClassifier(n_estimators=num_estimator, max_features='log2')
cv = clf.fit(features_data, abused_data)

dot_data = StringIO.StringIO()
tree.export_graphviz(clf.estimators_[20], out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_png("/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/randomForest.png")

appDataFile.close()