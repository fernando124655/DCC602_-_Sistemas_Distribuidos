# DCC602_-_Sistemas_Distribuidos
Repositório com algumas implementações da disciplina de Sistemas distribuídos

Estes códigos formam um sistema básico de detecção e resposta a incêndios utilizando Python e RabbitMQ para uma fila de mensagens para processamento em background. A temperatura da CPU é monitorada (producer.py), e se uma temperatura alta for detectada (temp-consumer.py), um alarme é disparado e o sistema de prevenção de incêndio é ativado (fire-alarm.py).

Para executar os arquivos python é nescessário ter o rabbitMQ, speech-dispatcher em seu linux. Além disso é necessário ter a biblioteca pika para comunicação com rabbitmq e a biblioteca psutil para recuperar informações do sistema.

OBS.: os 3 arquivos devem ser executados em simultâneo!