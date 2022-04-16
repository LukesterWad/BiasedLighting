import socket
from pickle import loads
import board
from neopixel import NeoPixel
from pathlib import Path
from json import load

try:
    with open(Path.home().joinpath(".config", "BiasedLighting.json"), "r") as file:
        data = load(file)
except FileNotFoundError:
    print("No configuration file detected.")
    exit()

PORT = 22047
GPIO_OUT = board.D18

try:
    HOST = data["host"]
    LED_COUNT = data["led count"]
except KeyError:
    print("Insuffiecient data. Requires 'host' and 'led count' fields.")
    exit()


pixels = NeoPixel(GPIO_OUT, LED_COUNT, auto_write=False)

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
                # Set the new colour for all lights in a frame.
                for cycle in range(LED_COUNT):
                    # Recieve data for processing.
                    data = client.recv(32)
                    # Send confirmation of reception.
                    client.send(b"0")

                    # Unpickle the recieved data.
                    data = loads(data)

                    # Assign the specified colour to the specified light.
                    pixels[data[0]] = data[1]

                pixels.show()

    except EOFError:
        print("Connection closed.")
    except socket.timeout:
        print("Timed out.")
