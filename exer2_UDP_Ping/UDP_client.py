
import socket
import time
from datetime import datetime

server_name = "localhost"
port = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)

i = 0

while True:
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Ping {i} {formatted_time}"
    try:
        print(f"Sending message to {server_name}:{port}")
        client_socket.sendto(message.encode(), (server_name, port))
        start_time = time.perf_counter()

        print("Waiting for response...")
        resp, addr = client_socket.recvfrom(1024)
        end_time = time.perf_counter()
        print(f"Received response: {resp.decode()}")
        print(f"Time elapsed: {end_time-start_time}s")

    except socket.timeout:
        end_time = time.perf_counter()
        print("No response received, request timed out.")
        print(f"Time elapsed: {end_time - start_time}s")

    finally:
        if i < 9:
            i = i + 1
        else:
            i = 0
        time.sleep(5)
client_socket.close()
