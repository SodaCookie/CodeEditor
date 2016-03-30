#!python3.4

import os
import sys
import traceback
from io import StringIO

from PyQt5 import QtGui, QtWidgets, QtCore

import codespace
import output

class CodeEditor(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cwd = ''

        # Handle window
        self.setWindowTitle('CodeEditor')
        self.resize(640, 480)

        # Add the menu bar
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        helpmenu = menubar.addMenu('&Help')

        # Open
        open_action = QtWidgets.QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        filemenu.addAction(open_action)

        # Save
        save_action = QtWidgets.QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        filemenu.addAction(save_action)

        # Exit
        exit_action = QtWidgets.QAction('&Exit', self)
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        filemenu.addAction(exit_action)

        # About
        about_action = QtWidgets.QAction('&About', self)
        about_action.triggered.connect(self.about_message)
        helpmenu.addAction(about_action)

        # Add the central widget
        self.main_window = QtWidgets.QWidget(parent)
        self.setCentralWidget(self.main_window)
        self.window_layout = QtWidgets.QVBoxLayout(self.main_window)

        self.code_space = codespace.CodeSpace(self.main_window)
        self.window_layout.addWidget(self.code_space)
        self.output = output.Output(self.main_window)
        self.window_layout.addWidget(self.output)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.run_button = QtWidgets.QPushButton("Run", self.main_window)
        self.button_layout.addWidget(self.run_button)
        self.clear_button = QtWidgets.QPushButton("Clear", self.main_window)
        self.button_layout.addWidget(self.clear_button)
        self.window_layout.addLayout(self.button_layout)

        self.run_button.clicked.connect(self.run_text)
        self.clear_button.clicked.connect(self.clear_text)

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open File", self.cwd, "PythonFiles (*.py);;All Files (*)")
        if file:
            self.clear_text()
            with open(file, "r") as prog_file:
                self.code_space.setText(prog_file.read())
                self.cwd = os.path.dirname(file)

    def save_file(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self,
            "Save File", self.cwd, "PythonFiles (*.py);;All Files (*)")
        if file:
            with open(file, "w") as prog_file:
                prog_file.write(self.code_space.toPlainText())
                self.cwd = os.path.dirname(file)

    def about_message(self):
        with open("ABOUT.txt", "r") as file:
            QtWidgets.QMessageBox.information(self, "About",
                file.read())

    def clear_text(self):
        self.code_space.clear()
        self.output.clear()

    def run_text(self):
        code = self.code_space.toPlainText()
        prev_stdout = sys.stdout
        prev_stderr = sys.stderr
        try:
            sys.stdout = StringIO()
            sys.stderr = sys.stdout
            exec(code)
        except Exception as e:
            traceback.print_exc()
        finally:
            self.output.setText(sys.stdout.getvalue())
            sys.stdout = prev_stdout
            sys.stderr = prev_stderr


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = CodeEditor()
    form.show()
    app.exec_()