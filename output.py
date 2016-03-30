from PyQt5 import QtCore, QtGui, QtWidgets

class Output(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)