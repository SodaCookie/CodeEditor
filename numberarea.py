from PyQt5 import QtGui, QtCore, QtWidgets

class NumberArea(QtWidgets.QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.lineNumberAreaWidth(), self.editor.height())

    def lineNumberAreaWidth(self):
        digits = len(str(self.editor.document().blockCount()))
        return 3 + QtGui.QFontMetrics(QtGui.QFont('latin1')).width('9') * digits

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setGeometry(0, 0, self.lineNumberAreaWidth(), self.height())
        self.editor.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.number_area.scroll(0, dy);
        else:
            self.number_area.update(0, rect.y(), self.number_area.width(),
                rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        self.setGeometry(QtCore.QRect(0,
            0, self.lineNumberAreaWidth(), self.editor.height()));

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(0, 0, self.lineNumberAreaWidth(), event.rect().height(), QtCore.Qt.lightGray)

        contents_y = self.editor.verticalScrollBar().value()
        font_metrics = self.fontMetrics()
        page_bottom = contents_y + self.editor.viewport().height()
        line_count = 0
        current_block = self.editor.document().findBlock(
            self.editor.textCursor().position())
        # Iterate over all text blocks in the document.
        block = self.editor.document().begin()
        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            position = self.editor.document().documentLayout().blockBoundingRect(block).topLeft()

            # Check if the position of the block is out side of the visible
            # area.
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            painter.drawText(self.lineNumberAreaWidth()//2 - font_metrics.width(str(line_count))//2, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            block = block.next()

        self.highest_line = line_count
        # block = self.firstVisibleBlock()
        # blockNumber = block.blockNumber()
        # top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        # bottom = top + self.blockBoundingRect(block).height()

        # while block.isValid() and top <= event.rect().bottom():
        #     if block.isVisible() and bottom >= event.rect().top():
        #         number = str(blockNumber + 1)
        #         painter.setPen(QtCore.Qt.black)
        #         painter.drawText(0, top, self.number_area.width(),
        #             self.fontMetrics().height(), QtCore.Qt.AlignRight, number)

        #     block = block.next()
        #     top = bottom
        #     bottom = top + self.blockBoundingRect(block).height()
        #     blockNumber += 1