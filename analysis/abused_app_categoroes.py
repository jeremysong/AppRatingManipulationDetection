import ast
from collections import defaultdict
import MySQLdb
import matplotlib.pyplot as plt
import numpy

__author__ = 'jeremy'

fig = plt.subplot()

bar_offset = -0.3

category_collection = list()

for location, db_name in [('itunes_us_data', 'Crawler_apple_us'), ('itunes_cn_data', 'Crawler_apple'), ('itunes_uk_data', 'Crawler_apple_uk')]:
    data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/' + location

    abused_app_file = open(data_path + '/abused_apps.txt', 'r')
    classified_app_file = open(data_path + '/classification_abused_app.txt', 'r')

    app_id_list = list()

    for abused_app_row in abused_app_file:
        app_id_list.append(abused_app_row.split('.')[1].strip())

    app_id_list.extend(ast.literal_eval(next(classified_app_file)))

    db = MySQLdb.connect(host='127.0.0.1', user='jeremy', passwd='ilovecherry', db=db_name)
    cur = db.cursor()
    app_data_sql_raw = "SELECT sub_category FROM AppData WHERE app_id='{}'"

    category_dict = defaultdict(int)

    for app_id in app_id_list:
        app_data_sql = app_data_sql_raw.replace('{}', app_id)
        cur.execute(app_data_sql)
        app_data_row = cur.fetchone()
        try:
            category = app_data_row[0]
            if category:
                category_dict[app_data_row[0]] += 1
        except TypeError:
            continue

    category_collection.append(category_dict)

categories = set()
[categories.add(category) for location in category_collection for category in location.keys()]
categories = list(categories)

us_y = [category_collection[0][key] for key in categories]
us_total = float(sum(us_y))
us_normalized_y = map(lambda m: m / us_total, us_y)
print(us_normalized_y)

cn_y = [category_collection[1][key] for key in categories]
cn_total = float(sum(cn_y))
cn_normalized_y = map(lambda m: m / cn_total, cn_y)
print(cn_normalized_y)

uk_y = [category_collection[2][key] for key in categories]
uk_total = float(sum(uk_y))
print(uk_total)
uk_normalized_y = map(lambda m: m / uk_total, uk_y)
print(uk_normalized_y)

us_bar = fig.bar(numpy.arange(1, len(categories) + 1) - 0.2, us_normalized_y, width=0.2, color='r')
cn_bar = fig.bar(numpy.arange(1, len(categories) + 1), cn_normalized_y, width=0.2, color='g')
uk_bar = fig.bar(numpy.arange(1, len(categories) + 1) + 0.2, uk_normalized_y, width=0.2, color='b')
fig.legend([us_bar, cn_bar, uk_bar], ['US', 'China', 'UK'])
plt.xticks(range(1, len(categories) + 1, 1), categories, rotation=60)
plt.xlim([1, len(categories) + 1])
plt.grid()
plt.show()