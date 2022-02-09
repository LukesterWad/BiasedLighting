from PIL.Image import Image

clr = tuple[int, int, int]


class ImageHandler:
    def __init__(self, zone_width: int, zone_height: int, performance_value: int):
        self.__WIDTH = zone_width
        self.__HEIGHT = zone_height
        self.__PERFORMANCE_JUMP = performance_value
        self.__PERFORMANCE_START = performance_value // 2
        total = 0
        for x in range(self.__PERFORMANCE_START, self.__WIDTH, self.__PERFORMANCE_JUMP):
            for y in range(self.__PERFORMANCE_START, self.__HEIGHT, self.__PERFORMANCE_JUMP):
                total += 1
        self.__TOTAL = total

    def setImage(self, image: Image): self.__image = image

    def getAverage(self) -> clr:
        r = g = b = 0
        # Iterate through some pixels in the image and sum their RGB values.
        for x in range(self.__PERFORMANCE_START, self.__WIDTH, self.__PERFORMANCE_JUMP):
            for y in range(self.__PERFORMANCE_START, self.__HEIGHT, self.__PERFORMANCE_JUMP):
                pixel = self.__image.getpixel((x, y))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
        # Return the mean of the color values for all the pixels sampled.
        return (
            r // self.__TOTAL,
            g // self.__TOTAL,
            b // self.__TOTAL
        )


class Buffer:
    __pointer = 0
    __data = []

    def __init__(self, length: int):
        self.__LENGTH = length
        for index in range(length):
            self.__data.append((0, 0, 0))

    # Replace the old color with the new one.
    def update(self, color: clr):
        self.__data[self.__pointer] = color

        self.__pointer += 1
        if self.__pointer == self.__LENGTH:
            self.__pointer = 0

    # Get the average color of currently stored values.
    def getAverage(self) -> clr:
        r = 0
        g = 0
        b = 0

        for index in range(self.__LENGTH):
            r += self.__data[index][0]
            g += self.__data[index][1]
            b += self.__data[index][2]

        return (
            r // self.__LENGTH,
            g // self.__LENGTH,
            b // self.__LENGTH
        )


class Zone:
    __lights = ()

    def __init__(self, x0: int, y0: int, x1: int, y1: int, buffer_length: int, performance_value: int):
        self.__X0 = x0
        self.__Y0 = y0
        self.__X1 = x1
        self.__Y1 = y1
        self.__image_handler = ImageHandler(
            x1 - x0 + 1,
            y1 - y0 + 1,
            performance_value
        )
        self.__buffer = Buffer(buffer_length)

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
        image_average = self.__image_handler.getAverage()
        self.__buffer.update(image_average)
        return self.__buffer.getAverage()
