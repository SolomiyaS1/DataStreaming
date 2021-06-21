from kafka_reader import MessageReader
from kafka_publisher import MessagePublisher
from DataStreaming.utils import create_logger
import ast
import translator
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = create_logger(__name__)

model_sentiment = SentimentIntensityAnalyzer()


def detect_sentiment(input_text, model=model_sentiment):
    return model.polarity_scores(input_text)


if __name__ == '__main__':
    twitter_reader = MessageReader("messages_with_language")
    data_publisher = MessagePublisher("messages_with_language_and_sentiment")
    message = {}
    for topic, value in twitter_reader.get_twits():
        value_dict = ast.literal_eval(value)
        logger.info("%s value=%s" % (topic, value))
        input_text = value_dict['text']
        detected_language = value_dict['language']
        if detected_language == 'en':
            detected_sentiment = detect_sentiment(input_text)
        else:
            text_translated = translator.translate2english(input_text, detected_language)
            detected_sentiment = detect_sentiment(text_translated)
        message["text"] = input_text
        message["language"] = detected_language
        message['sentiment'] = detected_sentiment
        data_publisher.publish_results(message)