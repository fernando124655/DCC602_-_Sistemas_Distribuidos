import socket
from threading import Thread
#import rsa

class Server:
    Clients = []
    
    #inicializa o servidor TCP
    def __init__(self, HOST, PORT):
        #self.public_key, self.private_key = rsa.newkeys(1024)  # Gera chaves RSA

        self.conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conection.bind((HOST, PORT))
        self.conection.listen(5) # max amount connections (5)
        
        print(f"Servidor iniciado em {HOST}:{PORT}")
        print("Servidor está esperando clientes se conectarem...")

    def listen(self):
        while True:
            #client_socket.send(self.public_key.save_pkcs1())
            client_socket, address = self.conection.accept()
            print("Conexão do cliente vindo de " + str(address))

            client_name = client_socket.recv(1024).decode() 
            client = {"client_name": client_name, "client_socket": client_socket}

            self.broadcast_message(client_name, client_name + " entrou no chat!")

            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        client_name = client["client_name"]
        client_socket = client["client_socket"] 
        while True:
            client_message = client_socket.recv(1024).decode()
            if client_message.strip() == client_name + ": bye" or not client_message.strip():	
                self.broadcast_message(client_name, client_name + " has left the chat.")
                Server.Clients.remove(client)
                client_socket.close()
                break
            else:
                #caso o cliente não saia do chat, o servidor recebe a mensagem e a retransmite
                self.broadcast_message(client_name, client_message)

    def broadcast_message(self, sender_name, message):
        for client in self.Clients:
            client_name = client["client_name"]
            client_socket = client["client_socket"]
            # Avoid sending the message back to the sender
            if client_name != sender_name:
                try:
                    client_socket.send(f"{message}".encode())
                except Exception as e:
                    print(f"Erro ao enviar mensagem para {client['client_name']}: {e}")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 5000  # Porta que o servidor vai escutar
    server = Server(HOST, PORT)
    server.listen()