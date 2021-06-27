from kafka import KafkaConsumer
from json import loads
from time import sleep
import pandas as pd
import requests
import json

REST_API_URL = 'https://api.powerbi.com/beta/8a68f26d-b270-4ef3-ae78-bd695a909445/datasets/007430c5-b02e-480c-a056-63ebcf1ff69c/rows?key=WGt%2Bv%2BdbSdrVQg2ohUi3RhCUzB6qGzcbuxb7JSMIBnnWeROMURB9VS9n80BqN%2BUEb3GinkbCodJIcrZou3JkXA%3D%3D'
HEADER = ["de", "ua", "it", "en", "ru"]


consumer = KafkaConsumer(
    'raw_messages',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

list_of_languages = {"de": 0, "ua": 0, "it": 0, "en": 0, "ru": 0}

for message in consumer:
    message = message.value

    list_of_languages[message['language']] += 1
    data_json = bytes(json.dumps(list_of_languages), encoding='utf-8')
    req = requests.post(REST_API_URL, data_json)
    print(json.dumps(list_of_languages))
    sleep(2)

