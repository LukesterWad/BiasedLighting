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

    def __writeFile(self) -> None:
        with open(self.__filename, "w") as file:
            dump(self.__data, file)

    def getCurrentId(self) -> int:
        return self.__data["presets"][self.__data["current"]]["id"]

    def setCurrent(self, preset_id: str) -> None:
        for index in range(len(self.__data["presets"])):
            if self.__data["presets"][index]["id"] == preset_id:
                self.__data["current"] = index

        self.__writeFile()

    def getFavouritesList(self) -> list:
        favourites = []
        for preset in self.__data["presets"]:
            if preset["favourite"]:
                favourites.append(preset)
        return favourites

    def getPresetsList(self) -> list:
        return self.__data["presets"]

    def getModesList(self) -> list:
        return self.__data["modes"]

    def getCurrentFavouriteStatus(self) -> bool:
        return self.__data["presets"][self.__data["current"]]["favourite"]

    def getCurrentMode(self) -> str:
        return self.__data["presets"][self.__data["current"]]["reaction mode"]

    def getCurrentBuffer(self) -> int:
        return self.__data["presets"][self.__data["current"]]["smoothness"]

    def setFavouriteStatus(self, status: bool) -> None:
        self.__data["presets"][self.__data["current"]]["favourite"] = status
        self.__writeFile()

    def setMode(self, mode: str) -> None:
        self.__data["presets"][self.__data["current"]]["reaction mode"] = mode
        self.__writeFile()

    def setBuffer(self, buffer: int) -> None:
        self.__data["presets"][self.__data["current"]]["smoothness"] = buffer
        self.__writeFile()

    def createNew(self) -> None:
        preset_id = 0
        preset_ids = tuple([preset["id"] for preset in self.__data["presets"]])
        while True:
            if preset_id in preset_ids:
                preset_id += 1
            else:
                break
        preset = self.__data["presets"][self.__data["current"]].copy()
        preset["id"] = preset_id
        preset["name"] = f"Preset {preset_id}"
        self.__data["presets"].append(preset)
        self.__writeFile()

    def removeCurrent(self) -> None:
        self.__data["presets"].pop(self.__data["current"])
        self.__data["current"] = 0

        self.__writeFile()


class SettingsManager:
    def __init__(self, filename: str) -> None:
        self.__filename = filename
        self.__data = self.__readFile()

    def __readFile(self) -> dict:
        with open(self.__filename, "r") as file:
            return load(file)

    def __writeFile(self) -> None:
        with open(self.__filename, "w") as file:
            dump(self.__data, file)

    def getBrightness(self) -> int:
        return self.__data["BRIGHTNESS"]

    def setBrightness(self, brightness: int) -> None:
        self.__data["BRIGHTNESS"] = brightness
        self.__writeFile()

    def getTopLights(self) -> int:
        return len(self.__data["EDGE_LIGHTS"]["top"])

    def getBottomLights(self) -> int:
        return len(self.__data["EDGE_LIGHTS"]["bottom"])

    def getLeftLights(self) -> int:
        return len(self.__data["EDGE_LIGHTS"]["left"])

    def getRightLights(self) -> int:
        return len(self.__data["EDGE_LIGHTS"]["right"])

    def setLightLayout(self, top: int, bottom: int, left: int, right: int) -> None:
        index = 0

        for edge, lights in (("right", right), ("top", top), ("left", left), ("bottom", bottom)):
            edge_lights_list = []
            for light in range(lights):
                edge_lights_list.append(index)
                index += 1
            if edge == "right" or edge == "top":
                edge_lights_list.reverse()
            self.__data["EDGE_LIGHTS"][edge] = edge_lights_list

        self.__writeFile()

    def getZoneXCount(self) -> int:
        return self.__data["HORIZONTAL_ZONE_COUNT"]

    def getZoneYCount(self) -> int:
        return self.__data["VERTICAL_ZONE_COUNT"]

    def setZoneXCount(self, zone_count: int) -> None:
        self.__data["HORIZONTAL_ZONE_COUNT"] = zone_count
        self.__writeFile()

    def setZoneYCount(self, zone_count: int) -> None:
        self.__data["VERTICAL_ZONE_COUNT"] = zone_count
        self.__writeFile()


class HomePage(Page):
    def __init__(self, parent: QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager

        self.__process = None

        self.__createStartStopButtons()
        self.__createPresetList()

    def refresh(self) -> None:
        self.__listFavourites()

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
        self.__listing = True

        self.__favourite_presets = self.__preset_manager.getFavouritesList()
        self.__preset_list.clear()

        current_id = self.__preset_manager.getCurrentId()
        for preset in self.__favourite_presets:
            list_item = QListWidgetItem(preset["name"], self.__preset_list)
            if preset["id"] == current_id:
                self.__preset_list.setCurrentItem(list_item)

        self.__listing = False

    def __selectPreset(self) -> None:
        if not self.__listing:
            index = self.__preset_list.selectedIndexes()[0].row()
            if self.__favourite_presets[index]["id"] != self.__preset_manager.getCurrentId():
                self.__preset_manager.setCurrent(
                    self.__favourite_presets[index]["id"]
                )


class PresetConfigurationPage(Page):
    def __init__(self, parent: QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager

        self.__createPresetDropdown()
        self.__createModeDropdown()
        self.__createAddRemoveButtons()
        self.__createFavouriteButton()
        self.__createBufferSlider()

    def refresh(self) -> None:
        self.__listPresets()
        self.__listModes()
        self.__setFavouriteIcon()
        self.__setBufferSliderValue()

    def __createPresetDropdown(self) -> None:
        self.__preset_selector = Dropdown(self)
        self.__preset_selector.move(32, 21)

        self.__preset_selector.currentIndexChanged.connect(self.__selectPreset)

        self.__listPresets()

    def __listPresets(self) -> None:
        # Prevent changing the current preset via changing the index.
        self.__listing = True

        self.__preset_selector.clear()

        presets = self.__preset_manager.getPresetsList()
        current_id = self.__preset_manager.getCurrentId()
        for index in range(len(presets)):
            self.__preset_selector.addItem(
                presets[index]["name"], presets[index]["id"])
            if presets[index]["id"] == current_id:
                self.__preset_selector.setCurrentIndex(index)

        self.__listing = False

    def __selectPreset(self) -> None:
        if not self.__listing:
            preset_id = self.__preset_selector.currentData(256)
            if preset_id != self.__preset_manager.getCurrentId():
                self.__preset_manager.setCurrent(preset_id)
            self.refresh()

    def __createModeDropdown(self) -> None:
        self.__mode_selector = Dropdown(self)
        self.__mode_selector.move(32, 139)

        self.__mode_selector.currentIndexChanged.connect(self.__selectMode)

        self.__listModes()

    def __listModes(self) -> None:
        self.__listing = True

        self.__mode_selector.clear()

        modes = self.__preset_manager.getModesList()
        current_mode = self.__preset_manager.getCurrentMode()
        for mode in modes:
            self.__mode_selector.addItem(mode)
            self.__mode_selector.setCurrentText(current_mode)

        self.__listing = False

    def __selectMode(self) -> None:
        if not self.__listing:
            mode = self.__mode_selector.currentText()
            if mode != self.__preset_manager.getCurrentMode():
                self.__preset_manager.setMode(mode)

    def __createAddRemoveButtons(self) -> None:
        add_button = MiniButton(self, "+")
        add_button.move(645, 21)
        remove_button = MiniButton(self, "-")
        remove_button.move(736, 21)

        add_button.clicked.connect(self.__addPreset)
        remove_button.clicked.connect(self.__removePreset)

    def __addPreset(self) -> None:
        self.__preset_manager.createNew()
        self.refresh()

    def __removePreset(self) -> None:
        if len(self.__preset_manager.getPresetsList()) > 1:
            self.__preset_manager.removeCurrent()
            self.refresh()

    def __createFavouriteButton(self) -> None:
        self.__favourite_button = MiniButton(
            self, "", QIcon("hollow_star.png"))
        self.__favourite_button.move(853, 21)

        self.__favourite_button.clicked.connect(self.__toggleFavouriteStatus)

    def __setFavouriteIcon(self) -> None:
        if self.__preset_manager.getCurrentFavouriteStatus():
            self.__favourite_button.setIcon(QIcon("star.png"))
        else:
            self.__favourite_button.setIcon(QIcon("hollow_star.png"))

    def __toggleFavouriteStatus(self) -> None:
        new_status = not self.__preset_manager.getCurrentFavouriteStatus()
        self.__preset_manager.setFavouriteStatus(new_status)
        self.__setFavouriteIcon()

    def __createBufferSlider(self) -> None:
        Label(self, "Smoothness").move(214, 295)

        Label(self, "1").move(50, 250)
        Label(self, "5").move(572, 250)

        self.__buffer_slider = Slider(self)
        self.__buffer_slider.setMinimum(1)
        self.__buffer_slider.setMaximum(5)
        self.__buffer_slider.move(97, 269)

        self.__setBufferSliderValue()

        self.__buffer_slider.sliderReleased.connect(self.__changeBuffer)

    def __setBufferSliderValue(self) -> None:
        self.__buffer_slider.setValue(
            self.__preset_manager.getCurrentBuffer()
        )

    def __changeBuffer(self) -> None:
        self.__preset_manager.setBuffer(self.__buffer_slider.value())


class SettingsPage(Page):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__settings_manager = SettingsManager("settings.json")

        self.__createBrightnessSlider()
        self.__createLightLayoutDiagram()
        self.__createZoneCountInput()

    def __createBrightnessSlider(self) -> None:
        Label(self, "Brightness Scalar").move(165, 82)

        Label(self, "0").move(50, 37)
        Label(self, "255").move(580, 37)

        self.__brightness_slider = Slider(self)
        self.__brightness_slider.setMinimum(0)
        self.__brightness_slider.setMaximum(255)
        self.__brightness_slider.move(100, 56)

        self.__setBrightnessSliderValue()

        self.__brightness_slider.sliderReleased.connect(
            self.__changeBrightness)

    def __setBrightnessSliderValue(self) -> None:
        self.__brightness_slider.setValue(
            self.__settings_manager.getBrightness()
        )

    def __changeBrightness(self) -> None:
        self.__settings_manager.setBrightness(self.__brightness_slider.value())

    def __createLightLayoutDiagram(self) -> None:
        Label(self, "Lights Layout").move(56, 185)

        box = QWidget(self)
        box.setFixedSize(427, 320)
        box.setAutoFillBackground(True)
        box.setStyleSheet("background-color: #C4C4C4")
        box.move(267, 253)

        Label(self, "Start ↑").move(572, 500)

        self.__right_input = IntegerInput(self)
        self.__top_input = IntegerInput(self)
        self.__left_input = IntegerInput(self)
        self.__bottom_input = IntegerInput(self)
        self.__right_input.move(704, 383)
        self.__top_input.move(433, 183)
        self.__left_input.move(162, 383)
        self.__bottom_input.move(433, 583)

        self.__right_input.returnPressed.connect(self.__changeLightLayout)
        self.__top_input.returnPressed.connect(self.__changeLightLayout)
        self.__left_input.returnPressed.connect(self.__changeLightLayout)
        self.__bottom_input.returnPressed.connect(self.__changeLightLayout)

        self.__setLightLayout()

    def __setLightLayout(self) -> None:
        self.__right_input.setText(
            str(self.__settings_manager.getRightLights()))
        self.__top_input.setText(
            str(self.__settings_manager.getTopLights()))
        self.__left_input.setText(
            str(self.__settings_manager.getLeftLights()))
        self.__bottom_input.setText(
            str(self.__settings_manager.getBottomLights()))

    def __changeLightLayout(self) -> None:
        try:
            self.__settings_manager.setLightLayout(
                int(self.__top_input.text()),
                int(self.__bottom_input.text()),
                int(self.__left_input.text()),
                int(self.__right_input.text())
            )
        except ValueError:
            self.__setLightLayout()

    def __createZoneCountInput(self) -> None:
        Label(self, "Zones X").move(760, 24)
        Label(self, "Zones Y").move(760, 164)

        self.__zones_x_input = IntegerInput(self)
        self.__zones_y_input = IntegerInput(self)
        self.__zones_x_input.move(760, 84)
        self.__zones_y_input.move(760, 224)

        self.__zones_x_input.returnPressed.connect(self.__changeZoneCountX)
        self.__zones_y_input.returnPressed.connect(self.__changeZoneCountY)

        self.__setZoneCount()

    def __setZoneCount(self) -> None:
        self.__zones_x_input.setText(
            str(self.__settings_manager.getZoneXCount()))
        self.__zones_y_input.setText(
            str(self.__settings_manager.getZoneYCount()))

    def __changeZoneCountX(self) -> None:
        try:
            self.__settings_manager.setZoneXCount(
                int(self.__zones_x_input.text()))
        except ValueError:
            self.__setZoneCount()

    def __changeZoneCountY(self) -> None:
        try:
            self.__settings_manager.setZoneYCount(
                int(self.__zones_y_input.text()))
        except ValueError:
            self.__setZoneCount()


if __name__ == "__main__":
    application = QApplication([])
    window = Window("BiasedLighting")

    preset_manager = PresetManager("presets.json")

    window.addPage("Home", HomePage(window.page_stack, preset_manager))
    window.addPage("Preset\nConfiguration",
                   PresetConfigurationPage(window.page_stack, preset_manager))
    window.addPage("Settings", SettingsPage(window.page_stack))

    window.show()
    application.exec()
