from time import sleep
import requests
import json
from kafka_reader import MessageReader
import ast

REST_API_URL_LANG = 'https://api.powerbi.com/beta/8a68f26d-b270-4ef3-ae78-bd695a909445/datasets/007430c5-b02e-480c-a056-63ebcf1ff69c/rows?key=WGt%2Bv%2BdbSdrVQg2ohUi3RhCUzB6qGzcbuxb7JSMIBnnWeROMURB9VS9n80BqN%2BUEb3GinkbCodJIcrZou3JkXA%3D%3D'
REST_API_URL_SENT = 'https://api.powerbi.com/beta/8a68f26d-b270-4ef3-ae78-bd695a909445/datasets/e1fad58f-12f1-4120-aff8-631570c1105e/rows?key=acr%2Bt%2BgGL3LJ3ZYFmjAGzA0zAYcSYPwFpcXAn5B%2BvHFfv5AhbcbZc2mcHdZe%2BBimua65f5j26etFER4gR%2FXRxQ%3D%3D'

messages_with_language_and_sentiment = MessageReader("messages_with_language_and_sentiment")
list_of_languages = {}
list_of_sentiments = {'negative': 0, 'positive': 0, 'neutral': 0, 'total': 0}
for topic, value in messages_with_language_and_sentiment.get_twits():
    value_dict = ast.literal_eval(value)
    if value_dict['language'] in list_of_languages.keys():
        list_of_languages[value_dict['language']] += 1
    else:
        list_of_languages[value_dict['language']] = 1
    language_json = bytes(json.dumps(list_of_languages), encoding='utf-8')
    req = requests.post(REST_API_URL_LANG, language_json)
    print(json.dumps(list_of_languages))
    sleep(2)
    if value_dict['sentiment']:
        if value_dict['sentiment']['compound'] >= 0.05:
            list_of_sentiments['positive'] += 1
        elif -0.05 < value_dict['sentiment']['compound'] < 0.05:
            list_of_sentiments['neutral'] += 1
        else:
            list_of_sentiments['negative'] += 1
    list_of_sentiments['total'] += 1
    sentiment_json = bytes(json.dumps(list_of_sentiments), encoding='utf-8')
    req_sent = requests.post(REST_API_URL_SENT, sentiment_json)
    print(json.dumps(list_of_sentiments))
