import pika
import time


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body))
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue='task_queue')
channel.basic_qos(prefetch_count=1)

print(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
