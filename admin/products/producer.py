import json

import pika

params = pika.URLParameters('amqps://bzhsieor:qwwiAqFgtq8T33wHI9_p3rBPgTvsYOa3@gerbil.rmq.cloudamqp.com/bzhsieor')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
