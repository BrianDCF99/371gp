import socket
import os

# Define the host and port
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Bind to the address
    server_socket.listen(1)           # Start listening for connections
    print(f'Server listening on {HOST}:{PORT}')

    # Accept incoming connections
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f'Connected by {addr}')
            request = conn.recv(1024).decode('utf-8')  # Receive the client request
            print(f'Request: {request}')

            # Extract the requested file from the request
            request_line = request.splitlines()[0]
            requested_file = request_line.split()[1]
            
            # If the request is for the root path "/", serve test.html
            if requested_file == "/":
                requested_file = "/test.html"

            # Remove leading "/" to access the file
            file_path = requested_file.lstrip("/")
            
            # Check if the file exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                # Send a 200 OK response
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + content
            else:
                # Send a 404 Not Found response if the file does not exist
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"

            # Send the response
            conn.sendall(response.encode('utf-8'))