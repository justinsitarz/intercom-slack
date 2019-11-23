import requests
import json
import datetime
import time
import pandas as pd 
import math
import config as cfg


def conversation_request(cfg):
    r = requests.get(url = cfg.config['intercom_conv_url'], headers = cfg.config['intercom_headers'])
    data = r.json()
    return data

def conversation_checker(data):
    print(cfg.config['wait_time'])
    for conversation in data['conversations']:
        if pd.notnull(conversation['waiting_since']):
            user_name       = get_user(conversation)
            waiting_since   = conversation['waiting_since']
            epoch_time      = int(time.time()) 
            initiated_by    = conversation['conversation_message']['delivered_as']
            wait_diff       = waiting_since -  conversation['created_at']
            time_waiting    = math.floor((epoch_time - waiting_since) / 60)
            if initiated_by == 'customer_initiated' and wait_diff < 50 and time_waiting >= cfg.config['wait_time']:
                slack_request(user_name, time_waiting, conversation['id'], epoch_time)

def get_user(conversation):
    user_id = conversation['conversation_message']['author']['id']
    s = requests.get(url = cfg.config['intercom_user_url'] + user_id, headers = cfg.config['intercom_headers'])
    user = s.json()
    return user['pseudonym']

def slack_request(user_name, time_waiting, conversation_id, epoch_time):
    post_data = {   'attachments': 
                    [
                        {   'fallback':     'There is a chat waiting',
                            'color':        '#808080',
                            'pretext':      'Incoming chat from ' + user_name,
                            'author_name':  'Chat from ' + user_name + ' has been waiting for ' + str(time_waiting) + ' minutes.',
                            'title':        'View conversation in Intercom',
                            'title_link':   'https://app.intercom.io/a/apps/ufsj0our/inbox/inbox/conversation/' + conversation_id,
                            'footer':       'Opsgenie',
                            'footer_icon':  'https://www.blendedperspectives.com/wp-content/uploads/2019/02/Opsgenie-icon.png',
                            'ts':           epoch_time
                        }
                    ]
                }
    requests.post(url = cfg.config['slack_url'], headers = cfg.config['slack_headers'], data = json.dumps(post_data))

data = conversation_request(cfg)
conversation_checker(data)

      