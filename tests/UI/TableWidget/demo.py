# coding: utf-8
import sys

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)

from verbiverse.CustomWidgets import WordsTable


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.table = WordsTable(self)
        self.layout.addWidget(self.table)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.resize(1000, 1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
