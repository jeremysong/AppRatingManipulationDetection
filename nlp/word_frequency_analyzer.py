from collections import Counter

__author__ = 'jeremy'


def word_freq_analyze(data_path, stop_words):
    abused_app_comment_word = open(data_path + 'abused_app_comment_word.txt')

    word_list = list()
    for line in abused_app_comment_word:
        word_list.append(line.strip())

    for (word, freq) in Counter(word_list).most_common(200):
        if word in stop_words:
            continue
        print((word, freq))


if __name__ == "__main__":
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/'

    custom_stop_words = {'like', 'play', 'wai', 'ha', 'it', 'thank', 'wish', 'make', 'review', 'download', 'us', 'get',
                         'them', 'becaus', 'lot', 'after', 'word', 'keep', 'abl', 'must', 'down', 'stop', 'put',
                         'everyth', 'over', 'come', 'we', 'though', 'without', 'while', 'card', 'who', 'off', 'differ',
                         'few', 'thing', 'which', 'stuff', 'player', 'hour', 'video', 'let', 'load', 'time', 'plai',
                         'work', 'them', 'alwai', 'through', 'control'}

    word_freq_analyze(__data_path + 'itunes_uk_data/', custom_stop_words)

