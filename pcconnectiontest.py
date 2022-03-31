from pickle import dumps
import socket
from datetime import datetime


LED_COUNT = 30
COLORS = (
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
)
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
            color = COLORS[datetime.now().second % len(COLORS)]
            for light in range(LED_COUNT):
                data = (light, color)

                # Pickle the data to send.
                data = dumps(data)
                # Send the data.
                connection.send(data)

                # Wait for confirmation of reception.
                connection.recv(1)
