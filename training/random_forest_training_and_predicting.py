"""
Trains with training data and predict the apps from sample_predict_app.csv
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
import csv

iTunesDataFolder = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'

trainingDataFile = open(iTunesDataFolder + "trainingData.csv", 'r')
appDataFile = open(iTunesDataFolder + "coefPosNegRatingsAppData.csv", 'r')
predictionDataFile = open(iTunesDataFolder + "sample_predict_apps.csv", 'r')

trainingDataCsv = csv.reader(trainingDataFile, delimiter=',')
appDataCsv = csv.reader(appDataFile, delimiter=',')
predictionCsv = csv.reader(predictionDataFile, delimiter=',')

trainingDataHeader = next(trainingDataCsv)
appDataHeader = next(appDataCsv)

features = ['max_neg_week', 'poisson_num_peaks', 'perc_neg_week', '5star_num', 'num_neg_week', '3star_num',
            'var_perc_3_star_rating_by_week_by_version', 'max_pos_week', 'var_perc_4_star_rating_by_week_by_version',
            'perc_max_neg_week', 'poisson_last_peak', 'var_perc_neg_rater_by_week', '2star_num', '4star_num',
            'var_perc_1_star_rating_by_week_by_version', 'var_avg_rating_by_week', 'var_avg_rating_by_week_by_version',
            'var_perc_4_star_rating_by_week', 'var_perc_2_star_rating_by_week_by_version', 'coef_1_5_rating_by_week',
            'var_perc_5_star_rating_by_week', 'var_perc_2_star_rating_by_week', 'var_perc_pos_rater_by_week',
            'var_perc_1_star_rating_by_week', 'coef_avg_rating_num_by_week', 'perc_max_pos_week',
            'var_perc_neg_rater_by_week_by_version', 'price', 'var_perc_pos_rater_by_week_by_version',
            'var_perc_5_star_rating_by_week_by_version', 'var_perc_3_star_rating_by_week',
            'coef_pos_neg_rating_by_week', '1star_num', 'perc_pos_week', 'num_neg_rater', 'coef_2_5_rating_by_week',
            'average_rating', 'num_extr_neg_rater', 'poisson_first_peak', 'num_pos_week', 'num_helpfulness', 'num_week',
            'num_pos_rater', 'perc_extr_neg_rater', 'coef_3_5_rating_by_week', 'perc_neg_rater', 'total_rater',
            'perc_extr_pos_rater', 'num_extr_pos_rater', 'var_num_rating_by_week', 'var_num_rating_by_week_by_version',
            'helpfulness_ratio_avg', 'perc_pos_rater', 'perc_helpfulness', 'num_dev'][-18:]

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

