###
# Only handle http text GET requests
# cache algorithm is very simple, no outdated check
###
# problem: i don't know why I can't create a new file and write it!!!!!! It drives me crazy for over 4 hours!!!!
# solve: u must close a file after u use it!!!!! using with statement can avoid this disturbing problem!!!

import os
from socket import *
import sys
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
    with open(target_file, "r") as f:
        data = f.read()
    context_len = len(data)
    completion.append(f"Content-Length: {context_len}\r\n".encode())
    completion.append("\r\n".encode())  # End of headers

    return completion

hostname = "localhost"
port = 8080
internet_port = 80

# if len(sys.argv) <= 1:
#     print('Usage : "python proxy_server.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#     sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((hostname, port))
tcpSerSock.listen(1)

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(f"Request from {addr} is:\n{message}") # request from origin request client
    # Extract the filename from the given message
    filename = message.split()[1].partition("//")[2].replace("/", "_")
    filename = filename.replace("http://", "", 1)
    filename = filename.replace("www.", "", 1)
    print(f"Request filename is {filename}")
    fileExist = "false"
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_path, "html_cache", filename)
    file_path = file_path + ".html"
    # print(file_path)
    try:
        # Check wether the file exist in the cache
        with open(file_path, "r") as f:
            outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        cmpl_header = html_header_gen(message.encode(), file_path)
        for lines in cmpl_header:
            tcpCliSock.send(lines)
        tcpCliSock.send(outputdata.encode())
        print('Read from cache.\n\n\n')
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            print(f"Cache miss, trying fetch data from {hostn}:{internet_port}")
            try:
                # Connect to the socket to port 80
                c.connect((hostn, internet_port))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                request_path = filename  # 确保路径正确
                request = f"GET /{request_path} HTTP/1.1\r\nHost: {hostn}\r\nConnection: close\r\n\r\n"
                fileobj.write(request.encode())
                # Read the response into buffer
                response_lines = fileobj.readlines()
                headers = {}
                # for line in response_lines:
                #     print(line.decode())
                for line in response_lines:
                    if line.__contains__(b"HTTP"):
                        continue
                    if line == b"\r\n":
                        break
                    # print(line.decode())
                    header_key, header_value = line.decode().split(":", 1)
                    headers[header_key.strip()] = header_value.strip()
                print(f"Response Headers:\n{headers}")
                # Create a new file in the cache for the requested file.
                store_path = os.path.join(root_path, "html_cache", filename) + ".html"
                body_index = response_lines.index(b"\r\n") + 1
                with open(store_path, "w") as f:
                    f.write("\n")
                    for items in response_lines[body_index:]:
                        f.write(items.decode())
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                cmpl_header = html_header_gen(b"", store_path)
                for lines in cmpl_header:
                    tcpCliSock.send(lines)
                with open(store_path, "r") as f:
                    outputdata = f.read()
                tcpCliSock.send(outputdata.encode())
                print('Read from remote server.\n\n\n')
            except Exception as e:
                print(e)
                # HTTP response message for file not found
                target_file = os.path.join(root_path, "html_cache", "404_not_found.html")
                with open(target_file, 'r') as f:
                    outputdata = f.read()  # Read entire content

                # Send HTTP header for 404 error
                completion = html_header_gen(b"", target_file, Error=True)
                for head_lines in completion:
                    tcpCliSock.send(head_lines)

                tcpCliSock.send(outputdata.encode())

                print("Error detected.\n\n\n")
        else:
            # HTTP response message for file not found
            target_file = os.path.join(root_path, "html_cache", "404_not_found.html")
            with open(target_file, 'r') as f:
                outputdata = f.read()  # Read entire content

            # Send HTTP header for 404 error
            completion = html_header_gen(b"", target_file, Error=True)
            for head_lines in completion:
                tcpCliSock.send(head_lines)

            tcpCliSock.send(outputdata.encode())

            print("Error detected.\n\n\n")
    finally:
        # Close the client and the server sockets
        tcpCliSock.close()
tcpSerSock.close()
sys.exit()  # Terminate the program after sending the corresponding data
