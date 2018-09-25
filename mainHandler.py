from maingui import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import subprocess
import sys
import os
import platform
from functions import *


class MainHandler(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        super().__init__()

        self.boxLog.setReadOnly(True)
        boxout = self.BoxOut()
        boxout.boxlog = self.boxLog
        sys.stdout = boxout

        #self.devicesBtn.clicked.connect(self.devices)
        #self.actionDevices.triggered.connect(self.devices)
        self.remotePath="/storage/1B5B-B117/test"
        self.connectBtn.clicked.connect(self.connectPhone)
        self.actionConnect.triggered.connect(self.connectPhone)
        
        self.uploadBtn.clicked.connect(self.uploadFile)
        self.actionUpload.triggered.connect(self.uploadFile)
        
        self.downloadBtn.clicked.connect(self.downloadFile)
        self.actionDownload.triggered.connect(self.downloadFile)
        
        self.selectBtn.clicked.connect(self.setFile)
        self.actionSelect.triggered.connect(self.setFile)

    class BoxOut:
        def write(self,txt):
            msg = str(txt)
            self.boxlog.appendPlainText(msg )
        def flush(self):
            pass
    def connectPhone(self):
        phone=self.adbCommand(["devices"])
        if phone=="List of devices attached\n\n":
            phone="No devices found - have you turned on USB debugging?"
        print(phone)
    def uploadFile(self):
        try:
            upload=self.adbCommand(["push", self.file, self.remotePath+self.fileType])
            txt="Trying to push to "+self.remotePath+self.fileType+"\n"+upload
        except:
            txt=sys.exc_info()[0].__name__+" - Make sure you have selected a file to upload"
        print(txt)
    def downloadFile(self):
        try:
            download = self.adbCommand(["pull", self.remotePath+self.fileType, self.file])
            txt = "Trying to pull from "+self.remotePath+self.fileType+"\n"+download
        except:
            txt = sys.exc_info()[0].__name__+" - Make sure you have selected a file to download"
        print(txt)
    def selectFile(self):
        return QFileDialog.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
    def setFile(self):
        self.file, discard=self.selectFile()
        self.fileType="."+self.file.split(".")[-1]
        print(self.file+" selected!")
    def adbCommand(self, command):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        path = os.path.dirname(os.path.realpath(__file__))
        path.replace("\\", "/")
        osType = platform.system()
        if osType in ["Windows","Darwin","Linux"]:
            if osType == "Windows":
                extension = ".exe"
            else:
                extension = ""
            subp = subprocess.run([path+"/{}/platform-tools/adb{}".format(osType,extension)] + command, cwd=path, universal_newlines=True, startupinfo=si)
        else:
            print("Error: OS not supported")
