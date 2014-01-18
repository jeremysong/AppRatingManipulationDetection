"""
Trains with training data and predict the apps from sample_predict_app.csv
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
import csv

trainingDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/posNegWeekAppData.csv", 'r')
predictionDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/sample_predict_apps.csv", 'r')

trainingDataCsv = csv.reader(trainingDataFile, delimiter=',')
appDataCsv = csv.reader(appDataFile, delimiter=',')
predictionCsv = csv.reader(predictionDataFile, delimiter=',')

trainingDataHeader = next(trainingDataCsv)
appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'total_rater', 'var_num_rating_by_week', 'perc_extr_pos_rater',
            'var_avg_rating_by_week', 'num_extr_pos_rater', 'num_pos_week', 'num_week', 'poisson_first_peak',
            'var_perc_5_star_rating_by_week', 'var_perc_1_star_rating_by_week', 'perc_max_pos_week',
            'perc_max_neg_week', 'num_neg_rater', 'perc_neg_week', 'perc_neg_rater', 'var_perc_4_star_rating_by_week',
            '2star_num', 'var_perc_2_star_rating_by_week', 'perc_helpfulness', 'poisson_last_peek',
            'var_perc_pos_rater_by_week', 'var_perc_3_star_rating_by_week', '3star_num', '4star_num',
            'var_perc_neg_rater_by_week', '1star_num', 'perc_pos_week', 'price', 'num_dev', 'max_pos_week',
            'helpfulness_ratio_avg', 'perc_extr_neg_rater', 'num_extr_neg_rater', 'num_helpfulness',
            'poisson_num_peaks', '5star_num', 'average_rating', 'num_neg_week', 'max_neg_week']

num_estimator = 25

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

clf = RandomForestClassifier(n_estimators=num_estimator, max_features='auto')
clf.fit(training_data, target_data)

### Prediction phase
prediction_app = [row[1] for row in predictionCsv]
prediction_data = [complete_app_data[app_id] for app_id in prediction_app]

prediction_target = clf.predict(prediction_data)

prediction_abused = [prediction_app[index] for index, target in enumerate(prediction_target) if target == 1]

print(prediction_abused)
print(len(prediction_abused))

