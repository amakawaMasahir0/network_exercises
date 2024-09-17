import os
import threading
from socket import *
from datetime import datetime

# 固定的监听端口
MAIN_SERVER_PORT = 8001
SERVER_NAME = "192.168.43.96"


# HTML 头生成器函数
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

    with open(target_file) as f:
        data = f.read()
    context_len = len(data)
    completion.append(f"Content-Length: {context_len}\r\n".encode())
    completion.append("\r\n".encode())

    return completion


# 处理客户端请求
def handle_client(client_socket, client_addr):
    try:
        message = client_socket.recv(2048)
        if message:
            filename = message.decode().split()[1]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            target_file = os.path.join(parent_dir, "webpage", filename[1:])

            try:
                with open(target_file) as f:
                    outputdata = f.readlines()
                completion = html_header_gen(message, target_file)

                for head_lines in completion:
                    client_socket.send(head_lines)

                for line in outputdata:
                    client_socket.send(line.encode())
                client_socket.send("\r\n".encode())

            except IOError:
                target_file = os.path.join(parent_dir, "webpage", "404_not_found.html")
                with open(target_file) as f:
                    outputdata = f.readlines()
                completion = html_header_gen(message, target_file, Error=True)

                for head_lines in completion:
                    client_socket.send(head_lines)
                for line in outputdata:
                    client_socket.send(line.encode())
                client_socket.send("\r\n".encode())
    finally:
        client_socket.close()


# 主服务器监听
def main():
    # 创建主服务器套接字，监听固定端口
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((SERVER_NAME, MAIN_SERVER_PORT))
    serverSocket.listen(5)
    print(f"Main server listening on port {MAIN_SERVER_PORT}...")

    while True:
        client_socket, addr = serverSocket.accept()
        print(f"Received connection from {addr}")

        # 启动新线程处理客户端请求
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    main()
