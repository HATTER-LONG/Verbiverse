from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import MenuAnimationType, RoundMenu


class CContexMenu(RoundMenu):
    """Label context menu"""

    def __init__(self, parent: QLabel):
        super().__init__("", parent)
        self.selectedText = parent.selectedText()

        self.copyAct = QAction(
            FIF.COPY.icon(),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self._onCopy,
        )
        self.selectAllAct = QAction(
            self.tr("Select all"), self, shortcut="Ctrl+A", triggered=self._onSelectAll
        )

    def _onCopy(self):
        QApplication.clipboard().setText(self.selectedText)

    def _onSelectAll(self):
        self.label().setSelection(0, len(self.label().text()))

    def label(self) -> QLabel:
        return self.parent()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self.label().hasSelectedText():
            self.addActions([self.copyAct, self.selectAllAct])
        else:
            self.addAction(self.selectAllAct)

        return super().exec(pos, ani, aniType)
