import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from kafka_reader import MessageReader
from kafka_publisher import MessagePublisher
from utils import create_logger
import spacy
import ast

logger = create_logger(__name__)

MODELS_NAMES = {
    'es': 'es_core_news_sm',
    'zh': 'zh_core_web_sm',
    'da': 'da_core_news_sm',
    'nl': 'nl_core_news_sm',
    'en': 'en_core_web_sm',
    'fr': 'fr_core_news_sm',
    'de': 'de_core_news_sm',
    'el': 'el_core_news_sm',
    'it': 'it_core_news_sm',
    'ja': 'ja_core_news_sm',
    'lt': 'lt_core_news_sm',
    'nb': 'nb_core_news_sm',
    'pl': 'pl_core_news_sm',
    'pt': 'pt_core_news_sm',
    'ro': 'ro_core_news_sm',
    'ru': 'ru_core_news_sm'
}
MODELS = {
    'es': spacy.load(MODELS_NAMES['es']),
    'zh': spacy.load(MODELS_NAMES['zh']),
    'da': spacy.load(MODELS_NAMES['da']),
    'nl': spacy.load(MODELS_NAMES['nl']),
    'en': spacy.load(MODELS_NAMES['en']),
    'fr': spacy.load(MODELS_NAMES['fr']),
    'de': spacy.load(MODELS_NAMES['de']),
    'el': spacy.load(MODELS_NAMES['el']),
    'it': spacy.load(MODELS_NAMES['it']),
    'ja': spacy.load(MODELS_NAMES['ja']),
    'lt': spacy.load(MODELS_NAMES['lt']),
    'nb': spacy.load(MODELS_NAMES['nb']),
    'pl': spacy.load(MODELS_NAMES['pl']),
    'pt': spacy.load(MODELS_NAMES['pt']),
    'ro': spacy.load(MODELS_NAMES['ro']),
    'ru': spacy.load(MODELS_NAMES['ru'])
}
print('Spacy models are loaded successfully')

def get_model_by_lang(language, models=MODELS):

    return models.get(language, models['en'])  # default language: English


def get_entities(input_text, model):

    doc = model(input_text)
    return [(X.text, X.label_) for X in doc.ents]

if __name__ == '__main__':
    twitter_reader = MessageReader("messages_with_language")
    data_publisher = MessagePublisher("messages_with_language_and_entities")
    message = {}
    for topic, value in twitter_reader.get_twits():
        value_dict = ast.literal_eval(value)
        logger.info("%s value=%s" % (topic, value))
        input_text = value_dict['text']
        detected_language = value_dict['language']
        spacy_model = get_model_by_lang(detected_language)
        detected_entities = get_entities(input_text, spacy_model)
        message["text"] = input_text
        message["language"] = detected_language
        message['entities'] = detected_entities
        data_publisher.publish_results(message)