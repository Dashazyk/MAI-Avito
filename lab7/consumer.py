from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

conf = None
with open("conf.json") as conf_file:
    conf = json.loads(conf_file.read())

s_brokers = []
for broker in conf['brokers']:
    s = f"{broker['host']}:{broker['port']}"
    print(s)
    s_brokers.append(s)

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
	'shu_topic',
    group_id='my-group',
    bootstrap_servers=s_brokers
)
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    
    
    json_msg = json.loads(message.value.decode('utf-8'))
    # print(json_msg['type'])

    if json_msg['type'] != 'message':
        payload = json_msg

        producer = KafkaProducer(bootstrap_servers=s_brokers)
        payload = json.dumps(payload)

        future = producer.send('dead_topic', payload.encode('utf-8'))

        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            log.exception()
    else:
        print('Done', flush=True)
        # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                        #   message.offset, message.key,
                                        #   message.value))
    
    
# consume earliest available messages, don't commit offsets
# KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# # consume json messages
# KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# # consume msgpack
# KafkaConsumer(value_deserializer=msgpack.unpackb)

# # StopIteration if no message after 1sec
# KafkaConsumer(consumer_timeout_ms=1000)

# Subscribe to a regex topic pattern
# consumer = KafkaConsumer()
# consumer.subscribe(topic='shu_topic')

# Use multiple consumers in parallel w/ 0.9 kafka brokers
# typically you would run each on a different server / process / CPU
# consumer1 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')
# consumer2 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')
