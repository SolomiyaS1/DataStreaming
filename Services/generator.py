from kafka_publisher import MessagePublisher
from source_data_handler import SourceDataHandler


if __name__ == "__main__":
    data = SourceDataHandler()
    data_publisher = MessagePublisher("raw_messages")

    data.prepare_dataset()
    messages_present = 1

    while messages_present:
        messages_present = data_publisher.publish_results(data.get_next_message())
