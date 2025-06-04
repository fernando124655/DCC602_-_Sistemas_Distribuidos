import socket
from threading import Thread
import os
import rsa

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))

        # Recebe a chave pública do servidor
        server_pubkey_data = self.socket.recv(1024)
        self.server_pubkey = rsa.PublicKey.load_pkcs1(server_pubkey_data)

        # Gera chave pública e privada do cliente
        self.public_key, self.private_key = rsa.newkeys(1024)

        # Envia a chave pública do cliente para o servidor
        self.socket.send(self.public_key.save_pkcs1())

        self.name = input("Digite seu nome: ")

        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_messages).start()
        self.send_messages()

    def send_messages(self):
        while True:
            client_input = input("")
            client_message = f"{self.name}: {client_input}"
            encrypted_message = rsa.encrypt(client_message.encode(), self.server_pubkey)
            self.socket.send(encrypted_message)

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.socket.recv(1024)
                if not encrypted_message:
                    os._exit(0)

                # Descriptografa com a chave privada do cliente
                decrypted_message = rsa.decrypt(encrypted_message, self.private_key).decode()
                print("\033[1;31;40m" + decrypted_message + "\033[0;0m")
            except Exception as e:
                print(f"Erro ao descriptografar mensagem: {e}")
                continue

if __name__ == '__main__':
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 5000         # Porta do servidor
    client = Client(HOST, PORT)