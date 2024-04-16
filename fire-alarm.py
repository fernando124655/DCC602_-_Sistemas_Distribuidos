import pika
import os

def callback_fire(ch, method, properties, body):
    print("Incêndio detectado! Disparando alarme...")

    # Aqui você pode adicionar a lógica para disparar o alarme sonoro ou luminoso
    os.system('spd-say "um incendio foi detectado"')

    # Após disparar o alarme, publica uma mensagem indicando que o sistema de prevenção de incêndio deve ser ativado
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='fire_prevention_activation')
    channel.basic_publish(exchange='', routing_key='fire_prevention_activation', body='Ativar sistema de prevenção de incêndio')
    print("Sistema de prevenção de incêndio deve ser ativado!!")
    connection.close()

def consume_fire_detection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='fire_detection')
    channel.basic_consume(queue='fire_detection', on_message_callback=callback_fire, auto_ack=True)
    print('Aguardando detecção de incêndio...')
    channel.start_consuming()

if __name__ == '__main__':
    consume_fire_detection()
