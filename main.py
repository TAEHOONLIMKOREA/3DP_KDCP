# importing the required libraries
from time import sleep
from json import dumps
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    my_producer = KafkaProducer(
        bootstrap_servers=['keties.iptime.org:55592'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    # Send messages
    my_producer.send('msgtest', 'Hello World!!')

    # Kafka broker에 연결합니다.
    consumer = KafkaConsumer(
        'msgtest',  # topic 이름
        bootstrap_servers=['keties.iptime.org:55592'],
        auto_offset_reset='earliest',  # 가장 처음부터 메시지를 받습니다.
        enable_auto_commit=True,  # 자동으로 offset을 commit합니다.
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        print(f"Received message: {message.value}")

    print("End!")
    # Close the Kafka producer connection
    my_producer.close()