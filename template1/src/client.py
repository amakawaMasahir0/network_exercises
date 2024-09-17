from socket import *

server_name = 'localhost'
server_port = 12000

# UDP
# client_socket = socket(AF_INET, SOCK_DGRAM)
# while True:
#     message = input("Input lowercase sentence: ")
#     client_socket.sendto(message.encode(), (server_name, server_port))
#     modified_message, server_addr = client_socket.recvfrom(2048)
#     print(modified_message.decode())
# TCP
while True:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    sentence = input("Input lowercase sentence: ")
    client_socket.send(sentence.encode())
    modified_sentence = client_socket.recv(1024)    # formal socket connection has been closed
    print(f"From server: {modified_sentence.decode()}")
    client_socket.close()
