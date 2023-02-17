import socket
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 8000
MAX_CLIENTS = 5

# Globals
clients = []
next_rank = 1
command_queue = []
lock = threading.Lock()

# Thread function to handle a client's connection
def handle_client(client_socket, client_address):
    global next_rank
    global command_queue

    # Assign a rank to the client
    client_rank = next_rank
    next_rank += 1

    # Add the client to the list of connected clients
    clients.append((client_socket, client_address, client_rank))

    # Send a welcome message to the client
    welcome_message = f"Welcome to the server! Your rank is {client_rank}."
    client_socket.sendall(welcome_message.encode())

    # Loop to receive data from the client
    while True:
        data = client_socket.recv(1024).decode().strip()

        if not data:
            # Client has disconnected
            break

        # Parse the data as a command and its rank
        try:
            command, rank_str = data.split(',')
            rank = int(rank_str)
        except ValueError:
            # Invalid command format
            continue

        if rank > client_rank:
            # Command is from a higher-ranked client, so add it to the command queue
            with lock:
                command_queue.append((command, rank))
        else:
            # Command is from a lower-ranked client or the client itself, so broadcast it to other clients
            message = f"Client {client_rank}: {command}"
            for c in clients:
                if c[2] != client_rank:
                    c[0].sendall(message.encode())
            # Send a response message to the client
            response_message = f"Command '{command}' executed."
            client_socket.sendall(response_message.encode())

    # Client has disconnected, so remove it from the list of connected clients and adjust the ranks of the remaining clients
    clients.remove((client_socket, client_address, client_rank))
    for i, c in enumerate(clients):
        if c[2] > client_rank:
            clients[i] = (c[0], c[1], c[2]-1)

    # Close the client socket
    client_socket.close()

# Thread function to handle command execution by high-rank clients
def execute_commands():
    global command_queue

    while True:
        if command_queue:
            with lock:
                # Find the highest-ranked command in the queue
                max_rank = max([c[1] for c in command_queue])
                max_commands = [c for c in command_queue if c[1] == max_rank]
                # Remove the command(s) from the queue
                command_queue = [c for c in command_queue if c not in max_commands]
            # Execute the highest-ranked command(s)
            for command, rank in max_commands:
                message = f"Command '{command}' executed by high-rank client {rank}."
                for c in clients:
                    if c[2] == rank:
                        c[0].sendall(message.encode())

# Main function to start the server
def main():
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    # Start the thread
        # Start the command execution thread
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()

    print(f"Server is running on {HOST}:{PORT}...")

    # Accept incoming connections
    while True:
        if len(clients) < MAX_CLIENTS:
            # Accept the connection
            client_socket, client_address = server_socket.accept()

            # Create a new thread to handle the client's connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

            print(f"New client connected: {client_address}")
        else:
            print(f"Maximum number of clients ({MAX_CLIENTS}) reached. Rejecting incoming connection...")

    # Close the server socket
    server_socket.close()

if __name__ == '__main__':
    main()
