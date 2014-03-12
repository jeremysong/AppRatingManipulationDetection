__author__ = 'jeremy'

import matplotlib.pyplot as plt
import numpy

########################################
# UK                                   #
# -------- Abused Apps ----------      #
# Rating: 1; Average length: 31.664549 #
# Rating: 2; Average length: 33.519432 #
# Rating: 3; Average length: 23.869728 #
# Rating: 4; Average length: 17.671688 #
# Rating: 5; Average length: 13.502022 #
# -------- Benign Apps ----------      #
# Rating: 1; Average length: 34.524075 #
# Rating: 2; Average length: 42.31347  #
# Rating: 3; Average length: 37.890728 #
# Rating: 4; Average length: 29.315454 #
# Rating: 5; Average length: 21.28221  #
########################################

# CN
# -------- Abused Apps ----------
# Rating: 1; Average length: 26.86928
# Rating: 2; Average length: 23.06482
# Rating: 3; Average length: 17.283073
# Rating: 4; Average length: 12.990744
# Rating: 5; Average length: 11.352028
# -------- Benign Apps ----------
# Rating: 1; Average length: 26.734064
# Rating: 2; Average length: 24.167343
# Rating: 3; Average length: 18.943998
# Rating: 4; Average length: 13.927623
# Rating: 5; Average length: 10.662776

# US
# -------- Abused Apps ----------
# Rating: 1; Average length: 27.712059
# Rating: 2; Average length: 27.04132
# Rating: 3; Average length: 18.118889
# Rating: 4; Average length: 14.03844
# Rating: 5; Average length: 11.47155
# -------- Benign Apps ----------
# Rating: 1; Average length: 33.487823
# Rating: 2; Average length: 40.23651
# Rating: 3; Average length: 34.380577
# Rating: 4; Average length: 25.81814
# Rating: 5; Average length: 18.57383

# Abused, benign
us_num_token_1 = (27.712059, 33.487823)
us_num_token_2 = (27.04132, 40.23651)
us_num_token_3 = (18.118889, 34.380577)
us_num_token_4 = (14.03844, 25.81814)
us_num_token_5 = (11.47155, 18.57383)

cn_num_token_1 = (26.86928, 26.734064)
cn_num_token_2 = (23.06482, 24.167343)
cn_num_token_3 = (17.283073, 18.943998)
cn_num_token_4 = (12.990744, 13.927623)
cn_num_token_5 = (11.352028, 10.662776)

uk_num_token_1 = (31.664549, 34.524075)
uk_num_token_2 = (33.519432, 42.31347)
uk_num_token_3 = (23.869728, 37.890728)
uk_num_token_4 = (17.671688, 29.315454)
uk_num_token_5 = (13.502022, 21.288211)

fig = plt.subplot()
fig.set_ylabel('Average Number of Tokens')
bar1 = fig.bar(numpy.arange(1, 3, 1) - 0.3, us_num_token_1, color='r', width=0.15)
bar2 = fig.bar(numpy.arange(1, 3, 1) - 0.15, us_num_token_2, color='g', width=0.15)
bar3 = fig.bar(numpy.arange(1, 3, 1), us_num_token_3, color='b', width=0.15)
bar4 = fig.bar(numpy.arange(1, 3, 1) + 0.15, us_num_token_4, color='grey', width=0.15)
bar5 = fig.bar(numpy.arange(1, 3, 1) + 0.3, us_num_token_5, color='brown', width=0.15)
fig.legend([bar1, bar2, bar3, bar4, bar5], ['1 star', '2 star', '3 star', '4 star', '5 star'])
plt.xlim(0, 3)
plt.xticks([1, 2], ['Abused', 'Benign'])
plt.grid()
plt.tight_layout()
plt.show()

fig = plt.subplot()
fig.set_ylabel('Average Number of Tokens')
bar1 = fig.bar(numpy.arange(1, 3, 1) - 0.3, uk_num_token_1, color='r', width=0.15)
bar2 = fig.bar(numpy.arange(1, 3, 1) - 0.15, uk_num_token_2 , color='g', width=0.15)
bar3 = fig.bar(numpy.arange(1, 3, 1), uk_num_token_3, color='b', width=0.15)
bar4 = fig.bar(numpy.arange(1, 3, 1) + 0.15, uk_num_token_4, color='grey', width=0.15)
bar5 = fig.bar(numpy.arange(1, 3, 1) + 0.3, uk_num_token_5, color='brown', width=0.15)
fig.legend([bar1, bar2, bar3, bar4, bar5], ['1 star', '2 star', '3 star', '4 star', '5 star'])
plt.xlim(0, 3)
plt.xticks([1, 2], ['Abused', 'Benign'])
plt.grid()
plt.tight_layout()
plt.show()

fig = plt.subplot()
fig.set_ylabel('Average Number of Tokens')
bar1 = fig.bar(numpy.arange(1, 3, 1) - 0.3, cn_num_token_1, color='r', width=0.15)
bar2 = fig.bar(numpy.arange(1, 3, 1) - 0.15, cn_num_token_2 , color='g', width=0.15)
bar3 = fig.bar(numpy.arange(1, 3, 1), cn_num_token_3, color='b', width=0.15)
bar4 = fig.bar(numpy.arange(1, 3, 1) + 0.15, cn_num_token_4, color='grey', width=0.15)
bar5 = fig.bar(numpy.arange(1, 3, 1) + 0.3, cn_num_token_5, color='brown', width=0.15)
fig.legend([bar1, bar2, bar3, bar4, bar5], ['1 star', '2 star', '3 star', '4 star', '5 star'])
plt.xlim(0, 3)
plt.xticks([1, 2], ['Abused', 'Benign'])
plt.grid()
plt.tight_layout()
plt.show()