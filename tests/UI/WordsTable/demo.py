# coding: utf-8
import sys

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
)

from qfluentwidgets import (
    TableWidget,
    isDarkTheme,
    setTheme,
    Theme,
    TableView,
    TableItemDelegate,
    setCustomStyleSheet,
)


class Demo(QWidget):
    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
