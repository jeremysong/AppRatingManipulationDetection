import ast
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'jeremy'

data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_uk_data/'

abused_num_token_rating_1 = open(data_path + 'abused_comment_length_3.txt', 'r')
benign_num_token_rating_1 = open(data_path + 'benign_comment_length_3.txt', 'r')

abused_num_token_list = ast.literal_eval(next(abused_num_token_rating_1))
benign_num_token_list = ast.literal_eval(next(benign_num_token_rating_1))

var_abused_num_token_1 = np.var(abused_num_token_list)
var_benign_num_token_1 = np.var(benign_num_token_list)

print(var_abused_num_token_1, var_benign_num_token_1)

plt.hist([abused_num_token_list, benign_num_token_list], bins=200, normed=1, label=['Abused', 'Benign'])
plt.legend()
plt.xlim([0, 200])
plt.show()