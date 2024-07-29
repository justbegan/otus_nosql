from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import time

bootstrap_servers = 'localhost:9092'
topic = 'topic1'

producer_conf = {
    'bootstrap.servers': bootstrap_servers
}

consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}


def produce_message(producer, topic, message):
    try:
        producer.produce(topic, value=message)
        producer.flush()
        print(f"Produced message: {message}")
    except KafkaException as e:
        print(f"Failed to produce message: {e}")


def consume_messages(consumer, topic):
    try:
        consumer.subscribe([topic])
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition: {msg.partition()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f"Consumed message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


def main():
    producer = Producer(producer_conf)
    consumer = Consumer(consumer_conf)
    produce_message(producer, topic, 'Hello, Kafka!')
    time.sleep(1)
    print("Consuming messages...")
    consume_messages(consumer, topic)


if __name__ == "__main__":
    main()
