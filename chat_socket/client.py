import socket
from threading import Thread
import os


class Client:

    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Digite seu nome: ")

        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.recieve_messages).start()
        self.send_messages()

    def send_messages(self):
        while True:
            client_input = input("")
            client_mensage = self.name +": " + client_input
            self.socket.send(client_mensage.encode())

    def recieve_messages(self):
        while True:
            server_mensage = self.socket.recv(1024).decode()
            if not server_mensage.strip():
                os._exit(0)
            print("\033[1;31;40m" + server_mensage + "\033[0;0m")


if __name__ == '__main__':
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 5000  # Porta que o servidor vai escutar
    client = Client(HOST, PORT)