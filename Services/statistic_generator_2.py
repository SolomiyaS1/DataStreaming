from time import sleep
import requests
import json
from kafka_reader import MessageReader
import ast

REST_API_URL_ENT = 'https://api.powerbi.com/beta/12b9a53e-70ad-4438-ace3-a8b16dc98ffc/datasets/47993496-f958-48bb-86bb-fa6bf5810e01/rows?key=%2Fsks6gNVTVI7Buo84WnWzrcW0MUlesakK56A2ZIRNro6op%2Bo33qaoMRMS5tRMKdr%2F7Qtefv45thymbQFiXvZ6Q%3D%3D'

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