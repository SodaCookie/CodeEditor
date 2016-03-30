from PyQt5 import QtCore, QtGui, QtWidgets

import highlighter
import numberarea

class CodeSpace(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = highlighter.Highlighter(self)
        self.number_area = numberarea.NumberArea(self)

        # Signals
        self.document().blockCountChanged[int].connect(
            self.number_area.updateLineNumberAreaWidth)
        self.document().blockCountChanged[int].connect(
            self.number_area.update)
        # self.document().blockCountChanged[int].connect(
        #     self.number_area.updateLineNumberArea)
        # self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.setViewportMargins(self.number_area.lineNumberAreaWidth(), 0, 0, 0)

    def paintEvent(self, event):
        super().paintEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.number_area.resizeEvent(event)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        self.number_area.repaint()