import socket
from pickle import loads

HOST = "192.168.0.14"
PORT = 22047

# Indefinitely attempt to connect to the server.
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # If no data is recieved within 2 seconds, try again with a new connection.
            client.settimeout(2)
            # Attempt to connect to the server.
            client.connect((HOST, PORT))

            # Indefinitely update the lights with the recieved data.
            while True:
                # Recieve data for processing.
                data = client.recv(32)
                # Send confirmation of reception.
                client.send(b"0")

                # Unpickle the recieved data.
                data = loads(data)
                print(data)
    except EOFError:
        print("Connection closed.")
    except socket.timeout:
        print("Timed out.")
