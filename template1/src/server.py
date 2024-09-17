from socket import *

server_port = 12000
server_name = "localhost"

# UDP
# server_socket = socket(AF_INET, SOCK_DGRAM)
# server_socket.bind((server_name, server_port))
# print("Server ready.")
#
# while True:
#     message, client_addr = server_socket.recvfrom(2048)
#     modified_message = message.decode().upper()
#     server_socket.sendto(modified_message.encode(), client_addr)

# TCP
server_socket = socket(AF_INET, SOCK_STREAM)    # create a "door" socket
server_socket.bind((server_name, server_port))
server_socket.listen(1)  # max number of connect request is 1
print("Server ready.")
while True:
    connection_sock, addr = server_socket.accept()  # create a unique socket when receive request
    sentence = connection_sock.recv(1024).decode()
    modified_sentence = sentence.upper()
    connection_sock.send(modified_sentence.encode())
    connection_sock.close() # then close it
