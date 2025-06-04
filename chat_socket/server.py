import socket
from threading import Thread
import rsa

class Server:
    Clients = []  # Lista de clientes conectados com seus sockets e chaves públicas
    
    def __init__(self, HOST, PORT):
        # Gera as chaves RSA do servidor
        self.public_key, self.private_key = rsa.newkeys(1024)

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((HOST, PORT))
        self.connection.listen(5)

        print(f"Servidor iniciado em {HOST}:{PORT}")
        print("Servidor está esperando clientes se conectarem...")

    def listen(self):
        while True:
            client_socket, address = self.connection.accept()

            # Envia a chave pública do servidor ao cliente
            client_socket.send(self.public_key.save_pkcs1())

            # Recebe a chave pública do cliente
            client_public_key_data = client_socket.recv(1024)
            client_public_key = rsa.PublicKey.load_pkcs1(client_public_key_data)

            print("Conexão do cliente vindo de " + str(address))

            # Recebe o nome do cliente (ainda em texto plano)
            client_name = client_socket.recv(1024).decode()
            client = {
                "client_name": client_name,
                "client_socket": client_socket,
                "client_public_key": client_public_key
            }

            self.broadcast_message(client_name, f"{client_name} entrou no chat!")

            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        client_name = client["client_name"]
        client_socket = client["client_socket"]

        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break

                # Descriptografa mensagem com a chave privada do servidor
                decrypted_message = rsa.decrypt(encrypted_message, self.private_key).decode()

                if decrypted_message.strip() == client_name + ": bye":
                    self.broadcast_message(client_name, f"{client_name} saiu do chat.")
                    Server.Clients.remove(client)
                    client_socket.close()
                    break
                else:
                    self.broadcast_message(client_name, decrypted_message)
            except Exception as e:
                print(f"Erro ao processar mensagem de {client_name}: {e}")
                continue

    def broadcast_message(self, sender_name, message):
        for client in self.Clients:
            if client["client_name"] != sender_name:
                try:
                    # Criptografa a mensagem com a chave pública do cliente destinatário
                    encrypted_message = rsa.encrypt(message.encode(), client["client_public_key"])
                    client["client_socket"].send(encrypted_message)
                except Exception as e:
                    print(f"Erro ao enviar mensagem para {client['client_name']}: {e}")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5000
    server = Server(HOST, PORT)
    server.listen()