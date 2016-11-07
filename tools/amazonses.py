"""
Sends email via Amazon SES
"""

__author__ = 'jeremy'

import boto.ses


def send_email(from_addr, to_addrs, subject, msg):
    conn = boto.ses.connect_to_region('us-east-1', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
                                      aws_secret_access_key='YOUR_AWS_SECRETE_ACCESS_KEY')
    conn.send_email(from_addr, subject, msg, to_addrs)


if __name__ == '__main__':
    __from_addr = 'jeremy.song@me.com'
    __to_addr = 'jeremy.ysong@gmail.com'
    __subject = 'Feature generator stopped'
    __msg = 'Hi!\n\nFeature generator has stopped.\n\nBest,\nYang Song'
    send_email(__from_addr, __to_addr, __subject, __msg)
