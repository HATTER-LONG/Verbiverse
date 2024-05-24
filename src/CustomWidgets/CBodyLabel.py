from CContexMenu import CContexMenu
from PySide6.QtCore import (
    QPoint,
    Qt,
    Slot,
)
from qfluentwidgets import BodyLabel


class CBodyLabel(BodyLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        menu = CContexMenu(parent=self)
        menu.exec(self.mapToGlobal(event))
