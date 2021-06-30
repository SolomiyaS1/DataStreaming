from time import sleep
import requests
import json
from kafka_reader import MessageReader
import ast

REST_API_URL_LANG = 'https://api.powerbi.com/beta/12b9a53e-70ad-4438-ace3-a8b16dc98ffc/datasets/0381c85f-face-4c5d-80cb-5141b796b346/rows?key=SU%2FVE0Oj5dSMhjo4calR1xZuYHdlLLhtzcmiy3Uw3q%2BzXlUn18B5s%2FizRhW9MPHnVw6cFYjmadR%2F%2FX31ITmSzw%3D%3D'
REST_API_URL_SENT = 'https://api.powerbi.com/beta/12b9a53e-70ad-4438-ace3-a8b16dc98ffc/datasets/244f97e4-3c19-476d-b969-f342c378a316/rows?key=EiNQ%2FHDlRaXC2f7EZGx%2BNpAEvqNOO7eevDGcdWuTz8mpyNR7kULHVtpzs36uFtVz58xyNgOkO0T13ZFw%2FwdAsA%3D%3D'

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
