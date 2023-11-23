import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.113.17.172'  # Replace with server's IP address
    port = 12345

    client_socket.connect((host, port))

    while True:
        start_node = input("Enter start node (A, B, C, ...): ")
        end_node = input("Enter end node (A, B, C, ...): ")

        # Send start and end node information to the server for path finding
        message = f"{start_node},{end_node}"
        client_socket.send(message.encode('utf-8'))

        # Receive shortest path information from the server
        received_data = client_socket.recv(1024).decode('utf-8')
        print(received_data)

    client_socket.close()

if __name__ == "__main__":
    start_client()
