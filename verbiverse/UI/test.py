from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QListWidgetItem, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    RoundMenu,
)
from test_ui import Ui_Form


class CTest(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)

        self.subtitel_browser.setText("test subtitle")

        widget = QListWidgetItem("test list")
        self.tab_widget.subtitle.addItem(widget)

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        menu = RoundMenu(parent=self)

        menu.addAction(
            QAction(
                FIF.ADD_TO.icon(),
                self.tr("test"),
                self,
                triggered=lambda: print("test"),
            )
        )
        menu.exec(self.mapToGlobal(event))
