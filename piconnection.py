import socket
from pickle import loads
import board
from neopixel import NeoPixel

HOST = "192.168.0.14"
PORT = 22047
GPIO_PIN = board.D18
LED_COUNT = 30

pixels = NeoPixel(GPIO_PIN, LED_COUNT, auto_write=False)

# Indefinitely attempt to connect to the server.
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # If the server cannot be connected to within 2 seconds, try again with a new socket.
            client.settimeout(2)
            # Attempt to connect to the server.
            client.connect((HOST, PORT))

            # Indefinitely update the lights with the recieved data.
            while True:
                # Set the new colours for all lights in a frame.
                for cycle in range(LED_COUNT):
                    # Recieve data for processing.
                    data = client.recv(32)
                    # Send confirmation of reception.
                    client.send(b"0")

                    # Unpickle the recieved data.
                    data = loads(data)

                    # Assign the specified colour to the specified light.
                    pixels[data[0]] = data[1]

                # Update all lights.
                pixels.show()

    except socket.timeout:
        print("Timeout.")
    except EOFError:
        print("Connection closed.")
    except KeyboardInterrupt:
        break
