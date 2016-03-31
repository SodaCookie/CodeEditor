from PyQt5 import QtCore, QtGui, QtWidgets

import highlighter
import numberarea

class CodeSpace(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabwidth = 4
        self.highlighter = highlighter.Highlighter(self)
        self.number_area = numberarea.NumberArea(self)

        # Handle Monospace and word wrap
        font = QtGui.QFont('Courier New', 10)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setCurrentFont(font)

        self.setLineWrapMode(QtWidgets.QTextEdit.FixedColumnWidth)
        self.setLineWrapColumnOrWidth(80)

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

    def tab_line_forward(self, blocks):
        """Tabs the given line as a block forward to the proper tab space"""
        original_position = self.textCursor().position()
        original_anchor = self.textCursor().anchor()
        for block in blocks:
            cursor = self.textCursor()
            text = block.text()
            position = block.position()
            leading_spaces = len(text) - len(text.lstrip())
            padding = self.tabwidth - leading_spaces % self.tabwidth
            cursor.setPosition(position)
            self.setTextCursor(cursor)
            self.textCursor().insertText(" " * padding)
            if position <= original_position:
                original_position += padding
            if position <= original_anchor:
                original_anchor += padding
        cursor = self.textCursor()
        cursor.setPosition(original_anchor)
        cursor.setPosition(original_position, 1)
        self.setTextCursor(cursor)

    def tab_line_back(self, blocks):
        """Tabs the given line as a block back to the proper tab space"""
        original_position = self.textCursor().position()
        original_anchor = self.textCursor().anchor()
        for block in blocks:
            cursor = self.textCursor()
            text = block.text()
            position = block.position()
            leading_spaces = len(text) - len(text.lstrip())
            if leading_spaces:
                padding = abs(leading_spaces % self.tabwidth - self.tabwidth)
                cursor.setPosition(position)
                cursor.setPosition(position + padding, 1)
                self.setTextCursor(cursor)
                self.textCursor().removeSelectedText()
                if position <= original_position:
                    original_position -= padding
                if position <= original_anchor:
                    original_anchor -= padding
        cursor = self.textCursor()
        cursor.setPosition(original_anchor)
        cursor.setPosition(original_position, 1)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            cursor = self.textCursor()
            blocks = []

            if cursor.hasSelection():
                first_block = self.document().findBlock(\
                    cursor.selectionStart()).blockNumber()
                last_block = self.document().findBlock(\
                    cursor.selectionEnd()).blockNumber()
                # Add blocks inclusive
                for i in range(first_block, last_block+1):
                    blocks.append(self.document().findBlockByNumber(i))
            else:
                blocks.append(cursor.block())

            self.tab_line_forward(blocks)
            return
        elif event.key() == QtCore.Qt.Key_Backtab:
            cursor = self.textCursor()
            blocks = []

            if cursor.hasSelection():
                first_block = self.document().findBlock(\
                    cursor.selectionStart()).blockNumber()
                last_block = self.document().findBlock(\
                    cursor.selectionEnd()).blockNumber()
                # Add blocks inclusive
                for i in range(first_block, last_block+1):
                    blocks.append(self.document().findBlockByNumber(i))
            else:
                blocks.append(cursor.block())

            self.tab_line_back(blocks)
            return
        super().keyPressEvent(event)