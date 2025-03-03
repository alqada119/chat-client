import socket

# UDP Server for Status Notifications
def udp_server():
    udp_ip = "127.0.0.1"
    udp_port = 8081
    buffer_size = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((udp_ip, udp_port))

    print(f"UDP Server is listening on {udp_ip}:{udp_port} for status notifications...")

    while True:
        message, addr = server.recvfrom(buffer_size)
        print(f"Received message from {addr}: {message.decode()}")
        # Process the message (status update)
        if message.decode().startswith("STATUS:"):
            status = message.decode().split(":")[1]
            print(f"User status updated: {status}")
        else:
            print("Invalid UDP message format.")

if __name__ == "__main__":
    udp_server()
