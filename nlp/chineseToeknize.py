import ast
import MySQLdb

__author__ = 'jeremy'


comment_sql_raw = "SELECT comment, comment_title FROM Comment WHERE app_id='{}'"


def fetch_comment(host, user, passwd, db_name, app_id_list, output_file):
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name)
    cur = db.cursor()

    for app_id in app_id_list:
        comment_sql = comment_sql_raw.replace('{}', app_id)
        cur.execute(comment_sql)

        for comment_row in cur.fetchall():
            comment = comment_row[0]
            comment_title = comment_row[1]
            raw_comment = comment + ' ' + comment_title + '\n'
            output_file.write(raw_comment)

if __name__ == '__main__':
    __data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/itunes_us_data/'
    __host = '127.0.0.1'
    __user = 'jeremy'
    __passwd = 'ilovecherry'
    __db_name = 'Crawler_apple_us'

    abused_app_file = open(__data_path + 'abused_apps.txt', 'r')
    app_data = open(__data_path + 'coefPosNegRatingsAppData.csv', 'r')
    suspicious_app_file = open(__data_path + 'classification_abused_app.txt', 'r')

    abused_app_comment_file = open(__data_path + 'abused_app_comment.txt', 'w')
    benign_app_comment_file = open(__data_path + 'benign_app_comment.txt', 'w')

    next(app_data)

    #benign_app_list = list()
    abused_app_list = list()
    total_app_set = set()

    # for benign_row in benign_app_file:
    #     benign_app_list.append(benign_row.split(',')[0])

    for app_data_row in app_data:
        total_app_set.add(app_data_row.split(',')[0])

    for abused_row in abused_app_file:
        abused_app_list.append(abused_row.split('.')[1].strip())

    abused_app_list.extend(ast.literal_eval(next(suspicious_app_file)))
    benign_app_list = list(set(total_app_set) - set(abused_app_list))

    fetch_comment(host=__host, user=__user, passwd=__passwd, db_name=__db_name, app_id_list=abused_app_list, output_file=abused_app_comment_file)
    fetch_comment(host=__host, user=__user, passwd=__passwd, db_name=__db_name, app_id_list=benign_app_list, output_file=benign_app_comment_file)

    abused_app_file.close()
    app_data.close()
    suspicious_app_file.close()
    abused_app_comment_file.close()
    benign_app_comment_file.close()