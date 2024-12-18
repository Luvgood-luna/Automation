# Create a chat room client-to-client

import socket
import threading

host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))
server.listen()

clients = []
aliases = []


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)


# Function to handle client connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, sender_socket=client)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            message = f'{alias} has left the chat room.'.encode('utf-8')
            broadcast(message, client)

            aliases.remove(alias)
            break


# Main function to receive the connection
def receive():
    try:
        while True:
            print("The server is running and listening...............")
            client, address = server.accept()
            print(f'Client connection established with {str(address)}')
            client.send("alias?".encode('utf-8'))
            alias = client.recv(1024)
            aliases.append(alias)
            clients.append(client)
            print(f"The alias of the client is {alias}".encode('utf-8'))
            message = f'{alias} has joined the chat room'.encode('utf-8')
            broadcast(message, client)

            client.send("you are now connected".encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
    except KeyboardInterrupt:
         print("\nServer shutting down...")
    finally:
        server.close()
        print("Server socket closed.")


if __name__ == "__main__":
    receive()