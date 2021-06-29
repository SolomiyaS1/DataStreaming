from time import sleep
import requests
import json
from kafka_reader import MessageReader
import ast

REST_API_URL_ENT = 'https://api.powerbi.com/beta/8a68f26d-b270-4ef3-ae78-bd695a909445/datasets/bbdd22c4-25f0-4434-a901-11e0767a7b15/rows?key=qDLGGAVK8ZatXK8OsZxrXiiqb2MJf%2FXay4pbklvJ%2BFxv0nDtcnV5Gb1yyhyvioFpKZZIyM5IoT%2FXhXfJqfvtUQ%3D%3D'

list_of_entities = {"person": 0, "organization": 0, "product": 0, "date": 0}
messages_with_entities = MessageReader("messages_with_language_and_entities")
for topic, value in messages_with_entities.get_twits():
    value_dict = ast.literal_eval(value)
    entities = [ent[1] for ent in value_dict['entities']]
    if 'PERSON' in entities:
        list_of_entities['person'] += entities.count('PERSON')
    if 'ORG' in entities:
        list_of_entities['organization'] += entities.count('ORG')
    if 'PRODUCT' in entities:
        list_of_entities['product'] += entities.count('PRODUCT')
    if "DATE" in entities:
        list_of_entities["date"] += entities.count("DATE")
    entities_json = bytes(json.dumps(list_of_entities), encoding='utf-8')
    req_ent = requests.post(REST_API_URL_ENT, entities_json)
    print(json.dumps(list_of_entities))
    sleep(2)