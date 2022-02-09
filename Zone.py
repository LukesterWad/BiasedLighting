class Zone:
    __lights = ()

    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.__X0 = x0
        self.__Y0 = y0
        self.__X1 = x1
        self.__Y1 = y1

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
