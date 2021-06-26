#%%
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from time import sleep
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML




consumer = KafkaConsumer(
    'raw_messages',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

list_of_languages = {}

for message in consumer:
    message = message.value

    # df = pd.DataFrame([list_of_languages])
    # df_unpivot = df.melt(var_name='language', value_name='msg_quantity')
    # fig, ax = plt.subplots(figsize=(15, 8))
    # ax.barh(df_unpivot['language'],df_unpivot['msg_quantity'])

    if message['language'] in list_of_languages:
        list_of_languages[message['language']] += 1
    else:
        list_of_languages[message['language']] = 1
        
    print(list_of_languages)