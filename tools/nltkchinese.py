# coding: utf8
import MySQLdb
import nltk

__author__ = 'jeremy'

db = MySQLdb.connect(host='127.0.0.1', user='jeremy', passwd='ilovecherry', db='Crawler_apple')
cur = db.cursor()
comment_content_sql = "SELECT comment FROM Comment LIMIT 10"
cur.execute(comment_content_sql)

for comment_row in cur.fetchall():
    content = comment_row[0]
    print(content)
    print(len(content))
    tokens = nltk.word_tokenize(content.decode('utf-8'))
    for token in tokens:
        print(len(token), token)