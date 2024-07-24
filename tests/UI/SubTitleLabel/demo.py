# coding: utf-8
import sys

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    Theme,
    setTheme,
)

from verbiverse.CustomWidgets import CSubtitleLabel


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = CSubtitleLabel(self)
        self.label.setText("this is a test message to check subtitle label")
        self.layout.addWidget(self.label)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.resize(500, 300)


def main():
    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
