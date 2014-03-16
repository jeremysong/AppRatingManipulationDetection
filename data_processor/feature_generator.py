"""
A complete procedure to generate data with features and training set. If you choose to build training set, make sure you
generate necessary peripheral files before running this program.

Please makes sure than total_rater value are correct. Or you have to rebuild it from comment table.

"""
from tools import amazonses

__author__ = 'jeremy'

import build_app_data_from_database
import build_complete_reviewer_data
import add_pos_neg_rater_to_reviewer
import add_extr_pos_neg_rater_to_reviewer
import add_dev_num_to_app_data
import add_pos_neg_rater_to_app_data
import add_helpfulness_to_app_data
import add_rating_variacne_by_week_to_app_data
import add_var_perc_pos_neg_rater_by_week_to_app_data
import add_possion_fit_to_app_data
import add_extr_pos_neg_rater_to_app_data
import add_pos_neg_week_to_app_data
import add_var_perc_pos_neg_rater_by_week_by_version_to_app_data
import add_rating_variance_by_week_by_version_to_app_data
import add_coef_pos_neg_rating_to_app_data
from datePatterns import DatePatterns


data_path = '/Users/jeremy/GoogleDrive/PSU/thesis/itunes_data/amazon_us_data/'
host = '127.0.0.1'
user = 'jeremy'
passwd = 'ilovecherry'
db_name = 'Crawler_amazon_us'
notification_switch = False
has_version = False  # Fetch data from database and write to files

if False:
    build_app_data_from_database.generate_app_data(data_path, host, user, passwd, db_name)
    build_complete_reviewer_data.generate_reviewer_data(data_path, host, user, passwd, db_name)

    # Add positive and negative rater features to reviewer data
    add_pos_neg_rater_to_reviewer.generate_features(data_path)
    add_extr_pos_neg_rater_to_reviewer.generate_features(data_path)

    add_dev_num_to_app_data.generate_features(data_path)
    add_pos_neg_rater_to_app_data.generate_features(data_path, host, user, passwd, db_name)
    add_helpfulness_to_app_data.generate_features(data_path, host, user, passwd, db_name)

    add_rating_variacne_by_week_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                              DatePatterns.amazon_date_pattern)
    add_var_perc_pos_neg_rater_by_week_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                                     DatePatterns.amazon_date_pattern)
    add_possion_fit_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                  DatePatterns.amazon_date_pattern)
    add_extr_pos_neg_rater_to_app_data.generate_features(data_path, host, user, passwd, db_name)
    add_pos_neg_week_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                   DatePatterns.amazon_date_pattern)
    add_var_perc_pos_neg_rater_by_week_by_version_to_app_data.generate_feature(data_path, host, user, passwd, db_name,
                                                                               DatePatterns.amazon_date_pattern,
                                                                               has_version=has_version)
    add_rating_variance_by_week_by_version_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                                         DatePatterns.amazon_date_pattern,
                                                                         has_version=has_version)

add_coef_pos_neg_rating_to_app_data.generate_features(data_path, host, user, passwd, db_name,
                                                      DatePatterns.amazon_date_pattern)

if notification_switch:
    from_addr = 'jeremy.song@me.com'
    to_addr = 'jeremy.ysong@gmail.com'
    subject = 'Feature generator stopped'
    msg = 'Hi!\n\nFeature generator has stopped.\n\nBest,\nYang Song'
    amazonses.send_email(from_addr, to_addr, subject, msg)