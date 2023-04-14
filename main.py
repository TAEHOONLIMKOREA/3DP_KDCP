# importing the required libraries
from time import sleep
from json import dumps
from kafka import KafkaProducer

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    my_producer = KafkaProducer(
        bootstrap_servers=['10.0.3.53:55592']
    )

    # Send messages
    for i in range(7):
        message = f"Message {i}"
        my_producer.send('my_topic', value=message)

    # Close the Kafka producer connection
    my_producer.close()