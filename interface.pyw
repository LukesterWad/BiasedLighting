import graphics as gui
import subprocess
import json


class PresetManager:
    __filepath = "presets.json"

    def __init__(self) -> None:
        with open(self.__filepath, "r") as file:
            self.__data = json.load(file)
        self.__current_preset_index = self.getPresetIndex(
            self.__data["current"])

    def updateFile(self) -> None:
        with open(self.__filepath, "w") as file:
            json.dump(self.__data, file)

    def setCurrentPreset(self, selection_id: int) -> None:
        exists = False
        for preset in self.__data["presets"]:
            if preset["id"] == selection_id:
                exists = True
                break
        if exists:
            self.__data["current"] = selection_id
            self.__current_preset_index = self.getPresetIndex(selection_id)
        else:
            raise KeyError("Cannot map ID to a preset.")

    def getCurrentPresetID(self) -> int:
        return self.__data["current"]

    def getPresetIndex(self, preset_id: int) -> int:
        index = 0
        for preset in self.__data["presets"]:
            if preset["id"] == preset_id:
                return index
            index += 1

    def changePresetOption(self, option_key: str, choice) -> None:
        self.__data["presets"][self.__current_preset_index][option_key] = choice

    def getCurrentPresetName(self) -> str:
        return self.__data["presets"][self.__current_preset_index]["name"]

    def getPresetNamesAndIds(self) -> list[tuple[str, int]]:
        presets = []
        for preset in self.__data["presets"]:
            presets.append((preset["name"], preset["id"], preset["favourite"]))
        favourites = []
        index = 0
        while index != len(presets):
            if presets[index][2]:
                preset = presets.pop(index)
                favourites.append(preset[:2])
            else:
                presets[index] = presets[index][:2]
                index += 1
        presets = sorted(presets, key=lambda x: x[0])
        favourites = sorted(favourites, key=lambda x: x[0])
        favourites.extend(presets)
        return favourites


class HomePage(gui.Page):
    def __init__(self, parent: gui.QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager

        self.__startstopButtons()
        self.__presetListLabel()

        self.__process = None

        # self.__directory = os.path.realpath(
        #     __file__).removesuffix("\\interface.pyw")

    def __startProcess(self) -> None:
        if self.__process == None:
            self.__process = subprocess.Popen(
                ["python", "main.py"])

    def __stopProcess(self) -> None:
        if self.__process != None:
            self.__process.kill()
            self.__process.wait()
            self.__process = None

    def __startstopButtons(self) -> None:
        start_button = gui.Button(self, "Start")
        start_button.move(80, 80)
        start_button.clicked.connect(self.__startProcess)
        # start_button.clicked.connect(lambda: self.__startProcess())
        stop_button = gui.Button(self, "Stop")
        stop_button.move(80, 400)
        stop_button.clicked.connect(self.__stopProcess)
        # start_button.clicked.connect(lambda: self.__startProcess())
        # TODO: connect buttons to their functions

    def __presetListLabel(self) -> None:
        preset_list_label = gui.LabelBox(self, "Favourites", 440, 80)
        preset_list_label.move(480, 40)


class PresetConfigurationPage(gui.Page):
    def __init__(self, parent: gui.QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager

        self.__preset_selector = self.__presetSelector()

    def __presetSelector(self) -> gui.Dropdown:
        preset_selector = gui.Dropdown(self)
        preset_selector.move(32, 21)
        for preset in self.__preset_manager.getPresetNamesAndIds():
            preset_selector.addPreset(preset[0], preset[1])
        preset_selector.textActivated.connect(self.__selectPreset)
        return preset_selector

    def __selectPreset(self) -> None:
        preset_id = self.__preset_selector.currentData()
        self.__preset_manager.setCurrentPreset(preset_id)


class SettingsPage(gui.Page):
    def __init__(self, parent: gui.QWidget, preset_manager: PresetManager) -> None:
        super().__init__(parent)
        self.__preset_manager = preset_manager
        gui.Label(self, "Settings")


if __name__ == "__main__":
    application = gui.QApplication([])
    window = gui.Window("BiasedLighting")

    preset_manager = PresetManager()

    window.addPage("Home", HomePage(window.page_stack, preset_manager))
    window.addPage("Preset\nConfiguration",
                   PresetConfigurationPage(window.page_stack, preset_manager))
    window.addPage("Settings", SettingsPage(window.page_stack, preset_manager))

    window.show()
    application.exec()
