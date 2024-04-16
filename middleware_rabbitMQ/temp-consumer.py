import pika

def callback_temperature(ch, method, properties, body):
    temperature = float(body)
    if temperature > 40:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='fire_detection')
        channel.basic_publish(exchange='', routing_key='fire_detection', body='Incêndio detectado!')
        print("Incêndio detectado! Mensagem publicada.")
        connection.close()

def consume_cpu_temperature():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='cpu_temperature')
    channel.basic_consume(queue='cpu_temperature', on_message_callback=callback_temperature, auto_ack=True)
    print('Aguardando temperatura da CPU...')
    channel.start_consuming()

if __name__ == '__main__':
    consume_cpu_temperature()
