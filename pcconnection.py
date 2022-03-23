import socket
from pickle import dumps

HOST = "192.168.0.14"
PORT = 22047

# Ensure the socket is closed when finished with.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Define which IPv4 addresses can connect and on which port.
    server.bind((HOST, PORT))
    # Initialise the listener.
    server.listen()

    # Wait for a connection request and accept it.
    connection, client = server.accept()

    # Ensure the connnection is closed when finished with.
    with connection:
        print(f"{client} connected.")

        while True:
            data = (0, (255, 0, 127))

            # Pickle the data to send.
            data = dumps(data)
            # Send the data.
            connection.send(data)

            # Wait for confirmation of reception.
            connection.recv(1)
