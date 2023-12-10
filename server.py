import socket
import timeit

# Define the graph (adjacency matrix representation)
graph = [
    [0, 3, 2, float('inf'), 4, 2],
    [float('inf'), 0, 1, 5, 2, 3],
    [float('inf'), float('inf'), 0, 3, 2, 4],
    [float('inf'), float('inf'), float('inf'), 0, 1, 5],
    [float('inf'), float('inf'), float('inf'), float('inf'), 0, 2],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 0]
]

node_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}

def dijkstra(graph, start):
    distances = {node: float('inf') for node in range(len(graph))}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = priority_queue.pop(0)

        if current_distance > distances[current_node]:
            continue

        for neighbor in range(len(graph[current_node])):
            weight = graph[current_node][neighbor]
            if weight != float('inf'):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    priority_queue.append((distance, neighbor))
                    priority_queue.sort()

    return distances

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

        start_label, end_label = received_data.split(',')  # Assuming client sends "start,end" for path finding

        start_node = node_mapping.get(start_label)
        end_node = node_mapping.get(end_label)

        if start_node is not None and end_node is not None:
            shortest_path_distances = dijkstra(graph, start_node)
            
            # Check if a valid path exists
            if shortest_path_distances[end_node] != float('inf'):
                shortest_path_distance = shortest_path_distances[end_node]
                print(f"Shortest path distance from {start_label} to {end_label}: {shortest_path_distance}")
                message = f"Shortest path distance from {start_label} to {end_label}: {shortest_path_distance}"
            else:
                message = f"No path exists from {start_label} to {end_label}"
        else:
            message = "Invalid node labels"
        
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    server_socket.close()

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

if __name__ == "__main__":
    server_overhead = measure_server_overhead()
    print(f"Overhead for server setup and teardown: {server_overhead} seconds")
    start_server()











