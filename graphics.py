from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QStackedWidget, QLabel


class Button(QPushButton):
    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(text, parent)
        self.setFixedSize(320, 240)
        self.setStyleSheet("background-color: #C4C4C4; font-size: 40px")


class Label(QLabel):
    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 40px")


class LabelBox(QWidget):
    def __init__(self, parent: QWidget, text: str, w: int, h: int) -> None:
        super().__init__(parent)
        self.setFixedSize(w, h)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #C4C4C4; font-size: 40px")

        self.label = Label(self, text)
        self.label.setFixedSize(w, h)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


class Page(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFixedSize(960, 720)


class PageStack(QStackedWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFixedSize(960, 720)

        self.__pages = []

    def showPage(self, page_index: int) -> None:
        self.setCurrentWidget(self.__pages[page_index])

    def addPage(self, page: Page) -> None:
        self.__pages.append(page)
        self.addWidget(page)

    def getPageCount(self) -> int:
        return len(self.__pages)


class NavigationButton(Button):
    def __init__(self, parent: QWidget, active: bool = False, text: str = "") -> None:
        super().__init__(parent, text)

        self.setActivity(active)

    def setActivity(self, active: bool) -> None:
        if active:
            self.setStyleSheet("background-color: #DDDDDD; font-size: 40px")
        else:
            self.setStyleSheet("background-color: #C4C4C4; font-size: 40px")


class NavigationButtonContainer(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFixedSize(320, 720)

        self.__buttons = []

    def addButton(self, button: NavigationButton) -> None:
        button.released.connect(
            # When released, change the appearance of all buttons accordingly.
            lambda: self.selectButton(button)
        )
        button.move(0, len(self.__buttons)*240)
        self.__buttons.append(button)

    def selectButton(self, sender: NavigationButton) -> None:
        for button in self.__buttons:
            button.setActivity(False)
        sender.setActivity(True)


class Window(QMainWindow):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setWindowTitle(title)

        self.__navigation_button_container = NavigationButtonContainer(self)

        self.page_stack = PageStack(self)
        self.page_stack.move(320, 0)

    def addPage(self, name: str, page: Page) -> None:
        # Add the page to the page stack.
        self.page_stack.addPage(page)

        page_count = self.page_stack.getPageCount()

        button = NavigationButton(
            self.__navigation_button_container,
            # Set only the first button to be active by default.
            page_count == 1,
            name
        )
        button.clicked.connect(
            # When clicked, show the corresponding page.
            lambda: self.page_stack.showPage(page_count - 1)
        )
        self.__navigation_button_container.addButton(button)
