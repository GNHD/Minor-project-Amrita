import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.113.17.172'  # Replace with the server's IP address or hostname
    port = 12345
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        start_node = input("Enter the start node (e.g., 'A'): ").upper()
        end_node = input("Enter the end node (e.g., 'D'): ").upper()

        # Send start and end nodes to the server
        message = f"{start_node},{end_node}"
        client_socket.send(message.encode('utf-8'))

        # Receive and print the response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    except ConnectionRefusedError:
        print("The server is not running or refused the connection.")

    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()