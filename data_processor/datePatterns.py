from enum import Enum

__author__ = 'jeremy'


class DatePatterns(Enum):
    """
    Enum type of data patterns including iTunes, amazon and windows app stores.
    """
    itunes_date_pattern = '%m/%d/%y'
    amazon_date_pattern = '%Y-%m-%d'
