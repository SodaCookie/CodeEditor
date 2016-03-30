import re
import keyword
import random

from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
        QMessageBox, QTextEdit)


class HighlightRule:

    def __init__(self, pattern, formats=None):
        """formats passed as a list"""
        self.pattern = pattern
        self.formats = []
        if formats:
            self.formats = formats

    def match(self, text, highlighter):
        for match in re.finditer(self.pattern, text):
            for i, format in enumerate(self.formats):
                if format:
                    start, end = match.span(i)
                    highlighter.setFormat(start, end - start, format)


class HighlightRuleRandomColours(HighlightRule):

    var_colours = {}
    var_patterns = []

    def __init__(self, pattern, var_group=1, formats=None):
        super().__init__(pattern, formats)
        self.var_group = var_group

    def match(self, text, highlighter):
        for match in re.finditer(self.pattern, text):
            for i, format in enumerate(self.formats):
                if format:
                    if i == self.var_group:
                        variable_name = match.group(i)
                        if self.var_colours.get(variable_name) == None:
                            self.var_colours[variable_name] = \
                                QTextCharFormat(format)
                            self.var_colours[variable_name].setForeground(
                                QColor(random.randint(0, 255),
                                           random.randint(0, 255),
                                           random.randint(0, 255)))
                            self.var_patterns.append(
                                re.compile(r"\b%s\b" % variable_name))
                    else:
                        start, end = match.span(i)
                        highlighter.setFormat(start, end - start, format)

        for var in self.var_patterns:
            for match in re.finditer(var, text):
                start, end = match.span()
                highlighter.setFormat(start, end - start,
                    self.var_colours[var.pattern.strip(r"\b")])


class Highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.darkBlue)
        keyword_format.setFontWeight(QFont.DemiBold)

        keywords = keyword.kwlist

        self.highlight_rules = [HighlightRule(re.compile(r"\b%s\b" % kword),
            [keyword_format]) for kword in keywords]

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.lightGray)
        comment_pattern = re.compile(r"#[^\n]*")
        self.highlight_rules.append(
            HighlightRule(comment_pattern, [comment_format]))

        function_format = QTextCharFormat()
        function_format.setForeground(Qt.blue)
        function_pattern = re.compile(r"def\b\s+([a-zA-Z][\w]+)")
        self.highlight_rules.append(
            HighlightRule(function_pattern, [None, function_format]))

        class_format = QTextCharFormat()
        class_format.setForeground(Qt.red)
        class_pattern = re.compile(r"class\b\s+([a-zA-Z][\w]+)")
        self.highlight_rules.append(
            HighlightRule(class_pattern, [None, class_format]))

        variable_format = QTextCharFormat()
        variable_format.setFontWeight(QFont.DemiBold)
        variable_pattern = re.compile(r"\b([a-zA-Z]\w*)\s*=\s*[^\n]+\b")
        self.highlight_rules.append(
            HighlightRuleRandomColours(variable_pattern, 1,
                [None, variable_format]))

        string_format = QTextCharFormat()
        string_format.setForeground(Qt.darkGreen)
        string_pattern = re.compile("'[^\n]*'|\"[^\n]*\"")
        self.highlight_rules.append(
            HighlightRule(string_pattern, [string_format]))

    def highlightBlock(self, text):
        for rule in self.highlight_rules:
            rule.match(text, self)
