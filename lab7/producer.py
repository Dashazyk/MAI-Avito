from kafka import KafkaProducer
from kafka.errors import KafkaError
import msgpack
import json
import sys

def send_string(producer, string, msg_type):
    payload = {'type': msg_type, 'message': string}

    payload = json.dumps(payload)

    future = producer.send('shu_topic', payload.encode('utf-8'))

    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()

def main(argv):
    conf = None
    with open("conf.json") as conf_file:
        conf = json.loads(conf_file.read())

    s_brokers = []
    for broker in conf['brokers']:
        s = f"{broker['host']}:{broker['port']}"
        print(s)
        s_brokers.append(s)
    producer = KafkaProducer(bootstrap_servers=s_brokers)
    send_string(producer, argv[2] if len(argv) > 2 else 'kya', argv[1] if len(argv) > 1 else 'message')


if __name__ == '__main__':
    main(sys.argv)
