"""
Find all the missing reviewer IDs in Reviewers table
"""

import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="jeremy", passwd="ilovecherry", db="Crawler_apple_us")
cur = db.cursor()
comment_sql = "SELECT reviewer_id FROM Comment"
reviewer_sql = "SELECT reviewer_id FROM Reviewers"

cur.execute(comment_sql)

reviewer_id_set_comment = set()
reviewer_id_set_reviewer = set()

for comment_row in cur.fetchall():
    reviewer_id_set_comment.add(comment_row[0])

cur.execute(reviewer_sql)

for reviewer_row in cur.fetchall():
    reviewer_id_set_reviewer.add(reviewer_row[0])

print(len(reviewer_id_set_comment))
print(len(reviewer_id_set_reviewer))

missing_reviewer_id = reviewer_id_set_comment - reviewer_id_set_reviewer

print(len(missing_reviewer_id))