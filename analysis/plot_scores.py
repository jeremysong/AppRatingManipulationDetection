import ast
import matplotlib.pyplot as plt

__author__ = 'jeremy'

score_file = open('/Users/jeremy/Desktop/new/itunes_uk_3.txt', 'r')

precision_list = list()
recall_list = list()
f_score_list = list()

calculate_f_score = True

for line in score_file:
    if line.startswith('('):
        score_tuple = ast.literal_eval(line)
        precision_list.append(score_tuple[0])
        recall_list.append(score_tuple[1])
        if calculate_f_score:
            f_score = 2*score_tuple[0]*score_tuple[1] / (score_tuple[0] + score_tuple[1])
            f_score_list.append(f_score)
        else:
            f_score_list.append(score_tuple[2])

x_range = range(55, 9, -1)

fig = plt.subplot()
fig.plot(x_range, precision_list, label='precision')
fig.plot(x_range, recall_list, label='recall')
fig.plot(x_range, f_score_list, label='f-score')
fig.set_ylabel('Scores')
fig.set_xlabel('Top N Features')
fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.grid()
plt.show()
