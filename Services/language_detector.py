from Services.kafka_reader import MessageReader
from Services.kafka_publisher import MessagePublisher
from utils import create_logger

logger = create_logger(__name__)


if __name__ == '__main__':
    twitter_reader = MessageReader("raw_messages")
    data_publisher = MessagePublisher("messages_with_language")
    message = {}
    for topic, value in twitter_reader.get_twits():
        logger.info("%s value=%s" % (topic, value))
        message["text"] = value
        message["language"] = "english"
        data_publisher.publish_results(message)
