from PIL.Image import Image

clr = tuple[int, int, int]


class ImageHandler:
    def __init__(self, zone_width: int, zone_height: int):
        self.__WIDTH = zone_width
        self.__HEIGHT = zone_height
        self.__TOTAL = zone_width * zone_height

    def setImage(self, image: Image): self.__image = image

    def getAverage(self) -> clr:
        r = g = b = 0
        # Iterate through each pixel in the image and sum their RGB values.
        for x in range(0, self.__WIDTH):
            for y in range(0, self.__HEIGHT):
                pixel = self.__image.getpixel((x, y))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
        # Return the mean of the color values for all the pixels in the image.
        return (
            r // self.__TOTAL,
            g // self.__TOTAL,
            b // self.__TOTAL
        )


class Zone:
    __lights = ()

    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.__X0 = x0
        self.__Y0 = y0
        self.__X1 = x1
        self.__Y1 = y1
        self.__image_handler = ImageHandler(
            x1 - x0 + 1,
            y1 - y0 + 1
        )

    # Evaluate equality as true if the zones have the same initial coordinates.
    # Overriding this method is acceptable becuse the "is" operator checks for two of the
    # same object.
    def __eq__(self, other: object) -> bool:
        return self.__X0 == other.__X0 and self.__Y0 == other.__Y0

    def getCoordinates(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (self.__X0,
             self.__Y0),
            (self.__X1,
             self.__Y1)
        )

    def setLights(self, lights: tuple): self.__lights = lights
    def getLights(self) -> tuple: return self.__lights

    def setImage(self, image: Image):
        # Assign a cropped image of the screen to the image handler.
        # The ending coordinates require a +1 as they represent the first pixels that
        # are not in the crop.
        self.__image_handler.setImage(
            image.crop((self.__X0, self.__Y0, self.__X1+1, self.__Y1+1))
        )

    def getColor(self) -> clr:
        return self.__image_handler.getAverage()
