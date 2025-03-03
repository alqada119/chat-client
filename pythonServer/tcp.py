import socket
import os

# TCP Server for Chat Messages and File Transfers
def tcp_server():
    tcp_ip = "127.0.0.1"
    tcp_port = 8082
    buffer_size = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((tcp_ip, tcp_port))
    server.listen(1)

    print(f"TCP Server is listening on {tcp_ip}:{tcp_port} for chat messages and file transfers...")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr} established.")

        # Receive the initial message type
        message = conn.recv(buffer_size).decode()
        
        if message.startswith("CHAT:"):
            print(f"Received chat message: {message}")
            conn.send(f"ACK:{message.split(':')[1]}".encode())  # Send acknowledgment
        elif message.startswith("FILE:"):
            file_info = message.split(":")
            sender_id = file_info[1]
            file_name = file_info[2]
            file_size = int(file_info[3])
            
            print(f"Received file transfer request: {file_name} ({file_size} bytes)")
            conn.send(f"ACK_FILE:{file_name}:{file_size}".encode())
            
            # Receive the file data in chunks
            with open(file_name, "wb") as f:
                remaining = file_size
                while remaining > 0:
                    data = conn.recv(min(remaining, buffer_size))
                    f.write(data)
                    remaining -= len(data)
            print(f"File {file_name} successfully received.")
        else:
            print("Invalid TCP message format.")
        conn.close()

if __name__ == "__main__":
    tcp_server()
