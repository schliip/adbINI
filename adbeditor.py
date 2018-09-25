#import adb3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from mainHandler import mainHandler

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    prog = mainHandler(window)
    SHOW = window.show()
    sys.exit(app.exec_())
