import pika
import psutil

# function to get the current temperature of the CPU
def get_cpu_temperature1():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
            temp_str = file.read().strip()
            return float(temp_str) / 1000  # Convertendo para Celsius
    except FileNotFoundError:
        print("Arquivo não encontrado:", '/sys/class/thermal/thermal_zone0/temp')
        return None
    except ValueError:
        print("Valor inválido no arquivo:", '/sys/class/thermal/thermal_zone0/temp')
        return None

#function to get the internal temperature of the encapsulation
def get_cpu_temperature2():
    temperaturas = psutil.sensors_temperatures()
    #lista de coretemp
    coretemps = temperaturas.get('coretemp', [])
    #percorrendo a lista procurando por package id 0
    package_temp = next((item for item in coretemps if item.label == 'Package id 0'), None)
    if package_temp:
        value = package_temp.current
        return value

def publish_cpu_temperature():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='cpu_temperature')
    temperature = get_cpu_temperature2()
    channel.basic_publish(exchange='', routing_key='cpu_temperature', body=str(temperature))
    print(f"Temperatura da CPU publicada: {temperature}")
    connection.close()

if __name__ == '__main__':
    publish_cpu_temperature()

    
