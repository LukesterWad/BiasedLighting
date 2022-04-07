from Zone import makeZones
import socket
from pickle import dumps
from json import load
from PIL.ImageGrab import grab


PORT = 22047

with open("settings.json", "r") as file:
    settings_data = load(file)

zones = makeZones(
    settings_data["SCREEN_WIDTH"],
    settings_data["SCREEN_HEIGHT"],
    settings_data["HORIZONTAL_ZONE_COUNT"],
    settings_data["VERTICAL_ZONE_COUNT"],
    settings_data["EDGE_LIGHTS"],
    settings_data["BUFFER_LENGTH"],
    settings_data["PERFORMANCE_VALUE"]
)


# Ensure the socket is closed when finished with.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Define which IPv4 addresses can connect and on which port.
    server.bind((settings_data["HOST"], PORT))
    # Initialise the listener.
    server.listen()

    # Wait for a connection request and accept it.
    connection, client = server.accept()

    # Ensure the connnection is closed when finished with.
    with connection:
        print(f"{client} connected.")

        while True:
            # Extract image data from the screen.
            image = grab()

            for zone in zones:
                zone.setImage(image)
                color = zone.getColor()

                for light in zone.getLights():
                    data = (light, color)

                    # Pickle the data to send.
                    data = dumps(data)
                    # Send the data.
                    connection.send(data)

                    # Wait for confirmation of reception.
                    connection.recv(1)
