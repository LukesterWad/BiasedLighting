from gui_components import *
import subprocess
from json import load, dump


class PresetManager:
    def __init__(self, filename: str) -> None:
        self.__filename = filename
        self.__data = self.__readFile()

    def __readFile(self) -> dict:
        with open(self.__filename, "r") as file:
            return load(file)

    def __writeFile(self, data: dict) -> None:
        with open(self.__filename, "w") as file:
            dump(data, file)

    def getFavourites(self) -> list:
        favourites = []
        for preset in self.__data["presets"]:
            if preset["favourite"]:
                favourites.append(preset)
        return favourites

    def setCurrent(self, preset_id: str) -> None:
        for index in range(len(self.__data["presets"])):
            if self.__data["presets"][index]["id"] == preset_id:
                self.__data["current"] = index

        self.__writeFile(self.__data)

    def getCurrentId(self) -> int:
        return self.__data["presets"][self.__data["current"]]["id"]


class HomePage(Page):
    def __init__(self, parent: QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager

        self.__process = None

        self.__createStartStopButtons()
        self.__createPresetList()

    def __createStartStopButtons(self) -> None:
        start_button = Button(self, "Start")
        start_button.move(80, 80)
        stop_button = Button(self, "Stop")
        stop_button.move(80, 400)

        start_button.clicked.connect(self.__startProcess)
        stop_button.clicked.connect(self.__stopProcess)

    def __startProcess(self) -> None:
        # If the process exists and has terminated.
        if self.__process != None:
            if self.__process.poll() != None:
                self.__process = subprocess.Popen(["python", "testing.py"])
        # If the process does not exists.
        else:
            self.__process = subprocess.Popen(["python", "testing.py"])

    def __stopProcess(self) -> None:
        # If the process exists and has not terminated.
        if self.__process != None and self.__process.poll() == None:
            self.__process.terminate()
            # Prevent Python from deleting the __process attribute from memory.
            self.__process = None

    def __createPresetList(self) -> None:
        LabelBox(self, "Favourites", 440, 80).move(480, 40)

        self.__preset_list = List(self)
        self.__preset_list.move(480, 120)

        self.__preset_list.itemSelectionChanged.connect(self.__selectPreset)

        self.__listFavourites()

    def __listFavourites(self) -> None:
        self.__favourite_presets = self.__preset_manager.getFavourites()
        self.__preset_list.clear()

        current_id = self.__preset_manager.getCurrentId()
        for preset in self.__favourite_presets:
            list_item = QListWidgetItem(preset["name"], self.__preset_list)
            if preset["id"] == current_id:
                self.__preset_list.setCurrentItem(list_item)

    def __selectPreset(self) -> None:
        index = self.__preset_list.selectedIndexes()[0].row()
        if self.__favourite_presets[index]["id"] != self.__preset_manager.getCurrentId():
            self.__preset_manager.setCurrent(
                self.__favourite_presets[index]["id"]
            )


class PresetConfigurationPage(Page):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.__createPresetDropdown()
        self.__createModeDropdown()
        self.__createAddRemoveButtons()
        self.__createFavouriteButton()
        self.__createBufferSlider()

    def __createPresetDropdown(self) -> None:
        preset_selector = Dropdown(self)
        preset_selector.move(32, 21)

        # # Insert method to change current preset.
        # preset_selector.currentIndexChanged.connect()

        # preset_selector.addItem("item 1", "some data 1")
        # preset_selector.addItem("item 2", "some data 2")
        preset_selector.addItem("item 1")
        preset_selector.addItem("item 2")

    def __createModeDropdown(self) -> None:
        mode_selector = Dropdown(self)
        mode_selector.move(32, 139)

        # mode_selector.addItem("item 1", "some data 1")
        # mode_selector.addItem("item 2", "some data 2")
        mode_selector.addItem("item 1")
        mode_selector.addItem("item 2")

    def __createAddRemoveButtons(self) -> None:
        add_button = MiniButton(self, "+")
        add_button.move(645, 21)
        remove_button = MiniButton(self, "-")
        remove_button.move(736, 21)

    def __createFavouriteButton(self) -> None:
        favourite_button = MiniButton(self, "", QIcon("star.png"))
        favourite_button.move(853, 21)

    def __createBufferSlider(self) -> None:
        Label(self, "Smoothness").move(214, 295)

        Label(self, "1").move(50, 250)
        Label(self, "5").move(572, 250)

        buffer_slider = Slider(self)
        buffer_slider.setMinimum(1)
        buffer_slider.setMaximum(5)
        buffer_slider.move(97, 269)


class SettingsPage(Page):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.__createBrightnessSlider()
        self.__createLightLayoutDiagram()
        self.__createZoneCountInput()

    def __createBrightnessSlider(self) -> None:
        Label(self, "Brightness Scalar").move(165, 82)

        Label(self, "0").move(50, 37)
        Label(self, "255").move(580, 37)

        brightness_slider = Slider(self)
        brightness_slider.setMinimum(0)
        brightness_slider.setMaximum(255)
        brightness_slider.move(100, 56)

    def __createLightLayoutDiagram(self) -> None:
        Label(self, "Lights Layout").move(56, 185)

        box = QWidget(self)
        box.setFixedSize(427, 320)
        box.setAutoFillBackground(True)
        box.setStyleSheet("background-color: #C4C4C4")
        box.move(267, 253)

        Label(self, "Start ↑").move(572, 500)

        right_input = IntegerInput(self)
        top_input = IntegerInput(self)
        left_input = IntegerInput(self)
        bottom_input = IntegerInput(self)
        right_input.move(704, 383)
        top_input.move(433, 183)
        left_input.move(162, 383)
        bottom_input.move(433, 583)

    def __createZoneCountInput(self) -> None:
        Label(self, "Zones X").move(760, 24)
        Label(self, "Zones Y").move(760, 164)

        zones_x_input = IntegerInput(self)
        zones_y_input = IntegerInput(self)
        zones_x_input.move(760, 84)
        zones_y_input.move(760, 224)


if __name__ == "__main__":
    application = QApplication([])
    window = Window("BiasedLighting")

    preset_manager = PresetManager("presets.json")

    window.addPage("Home", HomePage(window.page_stack, preset_manager))
    window.addPage("Preset\nConfiguration",
                   PresetConfigurationPage(window.page_stack))
    window.addPage("Settings", SettingsPage(window.page_stack))

    window.show()
    application.exec()
