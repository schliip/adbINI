from maingui import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import subprocess
import sys
import os
import platform

class mainHandler(Ui_MainWindow):
    def __init__(self, dialog):
        self.setupUi(dialog)
        self.boxLog.setReadOnly(True)
        Ui_MainWindow.__init__(self)
        self.osType=platform.system()
        
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
    def scrPrint(self, txt):
        msg = str(txt)
        self.boxLog.appendPlainText(msg+"\n")
    def devices(self):
        devices=self.adbCommand(["devices"])
        self.scrPrint(devices)
    def connectPhone(self):
        phone=self.adbCommand(["devices"])
        if phone=="List of devices attached\n\n":
            phone="No devices found - have you turned on USB debugging?"
        self.scrPrint(phone)
    def uploadFile(self):
        try:
            upload=self.adbCommand(["push", self.file, self.remotePath+self.fileType])
            txt="Trying to push to "+self.remotePath+self.fileType+"\n"+upload
        except:
            txt=sys.exc_info()[0].__name__+" - Make sure you have selected a file to upload"
        self.scrPrint(txt)
    def downloadFile(self):
        try:
            download=self.adbCommand(["pull", self.remotePath+self.fileType, self.file])
            txt="Trying to pull from "+self.remotePath+self.fileType+"\n"+download
        except:
            txt=sys.exc_info()[0].__name__+" - Make sure you have selected a file to download"
        self.scrPrint(txt)
    def selectFile(self):
        return QFileDialog.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
    def setFile(self):
        self.file, discard=self.selectFile()
        self.fileType="."+self.file.split(".")[-1]
        self.scrPrint(self.file+" selected!")   
    def adbCommand(self, command):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        path=os.path.dirname(os.path.realpath(__file__))
        path.replace("\\", "/")
        if self.osType=="Windows":
            subp=subprocess.run([path+"/windows/platform-tools/adb.exe"]+command, cwd=path, stdout=subprocess.PIPE, universal_newlines=True, startupinfo=si)
        elif self.osType=="Darwin":
            subp=subprocess.run([path+"/darwin/platform-tools/adb"]+command, cwd=path, stdout=subprocess.PIPE, universal_newlines=True, startupinfo=si)
        elif self.osType=="Linux":
            subp=subprocess.run([path+"/linux/platform-tools/adb"]+command, cwd=path, stdout=subprocess.PIPE, universal_newlines=True, startupinfo=si)
        else:
            self.scrPrint("Error: OS not supported")
        return subp.stdout
