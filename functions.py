import subprocess
import platform
import os


def adbCommand(self, command):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    path = os.path.dirname(os.path.realpath(__file__))
    path.replace("\\", "/")
    osType = platform.system()
    if osType in ["Windows", "Darwin", "Linux"]:
        if osType == "Windows":
            extension = ".exe"
        else:
            extension = ""
        subp = subprocess.run([path + "/{}/platform-tools/adb{}".format(osType, extension)] + command, cwd=path,
                              universal_newlines=True, startupinfo=si)
    else:
        print("Error: OS not supported")
