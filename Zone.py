class Zone:
    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.__X0 = x0
        self.__Y0 = y0
        self.__X1 = x1
        self.__Y1 = y1

    def getCoordinates(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (self.__X0,
             self.__Y0),
            (self.__X1,
             self.__Y1)
        )
