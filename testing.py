# import platform

# os_base = platform.system()
# if os_base == "Windows":
#     import wmi
#     import subprocess
#     import os

#     directory = os.path.realpath(__file__).removesuffix("\\testing.py")

#     # executable_name = "baisedlighting.exe"
#     executable_name = "main.exe"

#     process_manager = wmi.WMI()

#     def getProcess() -> wmi._wmi_object | None:
#         found_process = None
#         for process in process_manager.Win32_Process():
#             if process.name == executable_name:
#                 found_process = process
#                 break
#         return found_process

#     def endProcess() -> None:
#         process = getProcess()
#         if process != None:
#             process.Terminate()

#     def startProcess() -> None:
#         endProcess()
#         return subprocess.Popen([""])

if __name__ == "__main__":
    import subprocess
    import os

    directory = os.path.realpath(__file__).removesuffix("\\testing.py")
    executable = "\"" + directory + "\\dist\\main\\main.exe" + "\""
    print(executable)

    input()

    p = subprocess.Popen(["start", executable])

    input()

    p.terminate()
