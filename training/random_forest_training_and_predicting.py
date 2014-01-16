"""
Trains with training data and predict the apps from sample_predict_app.csv
"""

__author__ = 'jeremy'

from sklearn.ensemble import RandomForestClassifier
import csv

trainingDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/poissonAppData.csv", 'r')
predictionDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/sample_predict_apps.csv", 'r')

trainingDataCsv = csv.reader(trainingDataFile, delimiter=',')
appDataCsv = csv.reader(appDataFile, delimiter=',')
predictionCsv = csv.reader(predictionDataFile, delimiter=',')

trainingDataHeader = next(trainingDataCsv)
appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'var_num_rating_by_week', 'total_rater',
            'var_perc_4_star_rating_by_week', 'num_neg_rater', '4star_num', 'var_perc_5_star_rating_by_week',
            'var_avg_rating_by_week', 'num_week', 'perc_helpfulness', 'perc_neg_rater', 'var_perc_neg_rater_by_week',
            'var_perc_3_star_rating_by_week', 'helpfulness_ratio_avg', 'var_perc_2_star_rating_by_week',
            'var_perc_1_star_rating_by_week', 'num_dev', 'price', 'poisson_first_peak', 'poisson_last_peek',
            'var_perc_pos_rater_by_week', 'num_helpfulness', '1star_num', '5star_num', '3star_num', 'average_rating',
            'poisson_num_peaks', '2star_num']

num_estimator = 50

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

clf = RandomForestClassifier(n_estimators=num_estimator, max_features='log2')
clf.fit(training_data, target_data)

### Prediction phase
prediction_app = [row[1] for row in predictionCsv]
prediction_data = [complete_app_data[app_id] for app_id in prediction_app]

prediction_target = clf.predict(prediction_data)

prediction_abused = [prediction_app[index] for index, target in enumerate(prediction_target) if target == 1]

print(prediction_abused)
print(len(prediction_abused))

