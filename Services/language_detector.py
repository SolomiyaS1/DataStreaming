from kafka_reader import MessageReader
from kafka_publisher import MessagePublisher
from DataStreaming.utils import create_logger
import fasttext

logger = create_logger(__name__)

path_to_pretrained_model = '../Data/lid.176.bin'
fmodel = fasttext.load_model(path_to_pretrained_model)
print('FastText model is loaded successfully')


def detect_language(input_text, model=fmodel):

    clean_text = input_text.replace('\n', '')
    result = model.predict(clean_text)
    return result[0][0].split('__')[-1]  # language label with the highest probability


if __name__ == '__main__':
    twitter_reader = MessageReader("raw_messages")
    data_publisher = MessagePublisher("messages_with_language")
    message = {}
    for topic, value in twitter_reader.get_twits():
        logger.info("%s value=%s" % (topic, value))
        text = '  '.join(value.split('  ')[2:])
        message['id'] = int(value.split('  ')[0])
        message["text"] = text
        message["language"] = detect_language(text)
        data_publisher.publish_results(message)
