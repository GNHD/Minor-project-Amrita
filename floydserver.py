import socket
import timeit

# Define the graph (adjacency matrix representation)
graph = [
    [0, 3, 2, float('inf')],
    [float('inf'), 0, 1, 5],
    [float('inf'), float('inf'), 0, 3],
    [float('inf'), float('inf'), float('inf'), 0]
]

def floyd_warshall(graph):
    num_nodes = len(graph)

    # Perform Floyd-Warshall algorithm
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if graph[i][k] + graph[k][j] < graph[i][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]

    return graph

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    while True:
        received_data = client_socket.recv(1024).decode('utf-8')
        
        if not received_data:
            break

        start_node, end_node = received_data.split(',')  # Assuming client sends "start,end" for path finding
        start_node = ord(start_node) - ord('A')
        end_node = ord(end_node) - ord('A')

        distances = floyd_warshall(graph)

        shortest_path_distance = distances[start_node][end_node]
        message = f"Shortest path distance from {chr(start_node + ord('A'))} to {chr(end_node + ord('A'))}: {shortest_path_distance}"
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    server_socket.close()

# Function to measure execution time of server setup and teardown
def measure_server_overhead():
    setup_code = """
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    server_socket.close()
    client_socket.close()
"""
    stmt = "start_server()"
    time_taken = timeit.timeit(stmt, setup=setup_code, number=1)
    return time_taken

# Calculate overhead for server setup
server_overhead = measure_server_overhead()
print(f"Overhead for server setup and teardown: {server_overhead} seconds")

if __name__ == "__main__":
    start_server()

