from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    TransparentToolButton,
)


class CBaseWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setFixedWidth(450)
        self.vBoxLayout = QVBoxLayout(self)
        self.pin_button = TransparentToolButton(FIF.CLOSE, self)

        self.vBoxLayout.addWidget(self.pin_button, 0, Qt.AlignRight | Qt.AlignTop)
