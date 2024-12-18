# The client side script

import socket
import threading
from multiprocessing.reduction import send_handle
from pyexpat.errors import messages

alias = input('choose an alias >>>')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))

recv_thread = threading.Thread(target =client_recieve)
recv_thread.start()

send_thread = threading.Thread(target = client_send)
send_thread.start()