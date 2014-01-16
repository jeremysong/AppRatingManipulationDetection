__author__ = 'jeremy'

from sklearn import svm
from sklearn import cross_validation
import numpy as np
import csv
import random
import matplotlib.pylab as plt

appDataFile = open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/trainingData.csv", 'r')
appDataCsv = csv.reader(appDataFile, delimiter=',')

appDataHeader = next(appDataCsv)

features = ['num_pos_rater', 'perc_pos_rater', 'total_rater', 'var_perc_4_star_rating_by_week', 'num_neg_rater',
            'var_perc_5_star_rating_by_week', 'var_avg_rating_by_week', 'num_week', 'perc_helpfulness',
            'perc_neg_rater', 'var_perc_neg_rater_by_week', 'var_perc_3_star_rating_by_week', 'helpfulness_ratio_avg',
            'var_perc_2_star_rating_by_week', 'var_perc_1_star_rating_by_week', 'num_dev', 'price',
            'poisson_first_peak']

# scores_by_feature = list()

features_data = list()
abused_data = list()

feature_index = [appDataHeader.index(feature) for feature in features]

for app_data_row in appDataCsv:
    features_data.append([float(app_data_row[index]) for index in feature_index])
    abused_data.append(int(app_data_row[-1]))

clf = svm.LinearSVC()
#clf.fit(features_data[:5000], abused_data[:5000])
#predictions = clf.predict(features_data[5001:])
#scores = clf.score(features_data[5001:], abused_data[5001:])

random.seed()
cv = cross_validation.ShuffleSplit(len(features_data), n_iter=5, test_size=0.2, random_state=random.randint(1, 1000))
scores = cross_validation.cross_val_score(clf, np.array(features_data), np.array(abused_data), cv=cv, scoring='f1')

print(scores)
print('Average score:', np.average(scores))
# scores_by_feature.append(np.average(scores))

# appDataFile.seek(0)
# next(appDataCsv)

# plt.bar(np.arange(1, len(features), 1), scores_by_feature, align="center")
# plt.show()