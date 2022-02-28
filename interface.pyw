import graphics as gui
import subprocess
from os import path
# import os
# import json
#
#
# class PresetManager:
#     def __init__(self) -> None:
#         self.__directory =  \
#             os.path.realpath(__file__).removesuffix("utilities.py")
#         with open(f"{self.__directory}\\presets.json", "r") as file:
#             self.__data = json.load(file)

#     def writeData(self) -> None:
#         with open(f"{self.__directory}\\presets.json", "w") as file:
#             json.dump(self.__data, file)

#     def getPresetsList(self) -> list[dict]:
#         return self.__data["presets"]

#     def selectPreset(self, selection_id: int) -> None:
#         self.__data["current"] = selection_id


class HomePage(gui.Page):
    def __init__(self, parent: gui.QWidget) -> None:
        super().__init__(parent)

        self.__startstopButtons()
        self.__presetListLabel()

        self.__process = None

        directory = path.realpath(__file__).removesuffix("\\interface.pyw")
        # directory = path.realpath(__file__).removesuffix(
        #     "\\interface\\interface.exe")
        # self.__executable_path = f"\"{directory}\\dist\\main\\main.exe\""
        # self.__executable_path = f"\"{directory}\\main\\main.exe\""
        # print(self.__executable_path)

    def __startProcess(self) -> None:
        if self.__process == None:
            self.__process = subprocess.Popen(
                [self.__executable_path])

    def __stopProcess(self) -> None:
        if self.__process != None:
            self.__process.kill()
            self.__process = None

    def __startstopButtons(self) -> None:
        start_button = gui.Button(self, "Start")
        start_button.move(80, 80)
        start_button.clicked.connect(self.__startProcess)
        # start_button.clicked.connect(lambda: self.__startProcess())
        stop_button = gui.Button(self, "Stop")
        stop_button.move(80, 400)
        start_button.clicked.connect(self.__stopProcess)
        # start_button.clicked.connect(lambda: self.__startProcess())
        # TODO: connect buttons to their functions

    def __presetListLabel(self) -> None:
        preset_list_label = gui.LabelBox(self, "Favourites", 440, 80)
        preset_list_label.move(480, 40)


class PresetConfigurationPage(gui.Page):
    def __init__(self, parent: gui.QWidget) -> None:
        super().__init__(parent)
        gui.Label(self, "Preset Configuration")


class SettingsPage(gui.Page):
    def __init__(self, parent: gui.QWidget) -> None:
        super().__init__(parent)
        gui.Label(self, "Settings")


if __name__ == "__main__":
    application = gui.QApplication([])
    window = gui.Window("BiasedLighting")

    window.addPage("Home", HomePage(window.page_stack))
    window.addPage("Preset\nConfiguration",
                   PresetConfigurationPage(window.page_stack))
    window.addPage("Settings", SettingsPage(window.page_stack))

    window.show()
    application.exec()
