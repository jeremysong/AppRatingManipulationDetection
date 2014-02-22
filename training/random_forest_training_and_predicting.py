"""
Trains with training data and predict the apps from sample_predict_app.csv
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
import csv

iTunesDataFolder = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_cn_data/'

trainingDataFile = open(iTunesDataFolder + "trainingData.csv", 'r')
appDataFile = open(iTunesDataFolder + "coefPosNegRatingsAppData.csv", 'r')
predictionDataFile = open(iTunesDataFolder + "sample_predict_apps.csv", 'r')

trainingDataCsv = csv.reader(trainingDataFile, delimiter=',')
appDataCsv = csv.reader(appDataFile, delimiter=',')
predictionCsv = csv.reader(predictionDataFile, delimiter=',')

trainingDataHeader = next(trainingDataCsv)
appDataHeader = next(appDataCsv)

features = ['poisson_num_peaks', 'max_neg_week', 'num_neg_week', '1star_num', 'num_extr_neg_rater',
            'poisson_first_peak', 'var_perc_pos_rater_by_week', 'average_rating', 'var_perc_2_star_rating_by_week',
            'perc_extr_neg_rater', 'max_pos_week', 'perc_neg_week', 'perc_max_neg_week',
            'var_perc_neg_rater_by_week_by_version', '4star_num', 'perc_neg_rater', 'poisson_last_peak',
            'var_perc_2_star_rating_by_week_by_version', 'var_perc_3_star_rating_by_week_by_version',
            'perc_max_pos_week', 'var_perc_1_star_rating_by_week_by_version', 'num_helpfulness',
            'coef_2_5_rating_by_week', 'var_perc_4_star_rating_by_week_by_version', '5star_num', '3star_num',
            '2star_num', 'perc_pos_week', 'var_perc_pos_rater_by_week_by_version', 'var_perc_5_star_rating_by_week',
            'var_perc_4_star_rating_by_week', 'num_dev', 'var_perc_1_star_rating_by_week', 'var_perc_neg_rater_by_week',
            'helpfulness_ratio_avg', 'num_neg_rater', 'var_avg_rating_by_week',
            'var_perc_5_star_rating_by_week_by_version', 'price', 'var_avg_rating_by_week_by_version', 'num_pos_week',
            'coef_3_5_rating_by_week', 'var_perc_3_star_rating_by_week', 'num_week', 'coef_1_5_rating_by_week',
            'perc_helpfulness', 'coef_pos_neg_rating_by_week', 'coef_avg_rating_num_by_week', 'num_extr_pos_rater',
            'num_pos_rater', 'total_rater', 'var_num_rating_by_week', 'perc_extr_pos_rater',
            'var_num_rating_by_week_by_version', 'perc_pos_rater'][-25:]

num_estimator = 91

feature_index = [appDataHeader.index(feature) for feature in features]

### Building total data set containing all features
complete_app_data = dict()

for app_data_row in appDataCsv:
    complete_app_data[app_data_row[0]] = [float(app_data_row[index]) for index in feature_index]

### Training phase
training_data = list()
target_data = list()
for training_data_row in trainingDataCsv:
    training_data.append([float(training_data_row[index]) for index in feature_index])
    target_data.append(int(training_data_row[-1]))

clf = RandomForestClassifier(n_estimators=num_estimator, oob_score=True, min_samples_leaf=3)
clf.fit(training_data, target_data)

### Prediction phase
prediction_app = [row[1] for row in predictionCsv]
prediction_data = [complete_app_data[app_id] for app_id in prediction_app]

prediction_target = clf.predict(prediction_data)

prediction_abused = [prediction_app[index] for index, target in enumerate(prediction_target) if target == 1]

print(prediction_abused)
print(len(prediction_abused))
print('Total app: {0}'.format(len(prediction_data)))

