import os
from socket import *
from datetime import datetime


def html_header_gen(message, target_file, Error=False):
    completion = []
    try:
        http_version = message.decode().split()[2]
    except IndexError:
        http_version = "HTTP/1.1"

    if not Error:
        completion.append(f"{http_version} 200 OK\r\n".encode())
    else:
        completion.append(f"{http_version} 404 Not Found\r\n".encode())

    formated_utc_time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    completion.append(f"Date: {formated_utc_time}\r\n".encode())
    completion.append("Content-Type: text/html; charset=UTF-8\r\n".encode())
    # NOTICE: content-Length is string number, not file size(os.path.filesize(file))
    # this can cause http error, and no html body would present
    with open(target_file) as f:
        data = f.read()
    context_len = len(data)
    completion.append(f"Content-Length: {context_len}\r\n".encode())
    completion.append("\r\n".encode())  # End of headers

    return completion


server_port = 8080
server_name = "localhost"

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((server_name, server_port))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(2048)

    if message:
        filename = message.decode().split()[1]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        target_file = os.path.join(parent_dir, "webpage", filename[1:])

        try:
            with open(target_file, 'r') as f:
                outputdata = f.read()  # Read entire content

            # Send HTTP header
            completion = html_header_gen(message, target_file)
            for head_lines in completion:
                connectionSocket.send(head_lines)

            # Send the content of the requested file
            connectionSocket.send(outputdata.encode())

        except IOError:
            target_file = os.path.join(parent_dir, "webpage", "404_not_found.html")
            with open(target_file, 'r') as f:
                outputdata = f.read()  # Read entire content

            # Send HTTP header for 404 error
            completion = html_header_gen(message, target_file, Error=True)
            for head_lines in completion:
                connectionSocket.send(head_lines)

            connectionSocket.send(outputdata.encode())

        finally:
            connectionSocket.close()
    else:
        print("Empty request.")
        connectionSocket.close()
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data

