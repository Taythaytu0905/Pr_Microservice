import json

import pika

from main import Product, db

params = pika.URLParameters('amqps://bzhsieor:qwwiAqFgtq8T33wHI9_p3rBPgTvsYOa3@gerbil.rmq.cloudamqp.com/bzhsieor')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data.get('id'), title=data.get('title'), image=data.get('image'))
        db.session.add(product)
        db.session.commit()
        print('product_created')
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data.get('title')
        product.image = data.get('image')
        db.session.commit()
        print('product_updated')
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product_deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
